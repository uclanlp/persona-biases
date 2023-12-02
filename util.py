"""Common functions."""
import torch
import openai
from ratelimiter import RateLimiter
from retrying import retry
import re
import backoff
from transformers import StoppingCriteria, StoppingCriteriaList

openai.organization= $OPENAI_ORGANIZATION$
openai.api_key = $OPENAI_API_KEY$

class StopOnTokens(StoppingCriteria):
	def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
		stop_ids = [50278, 50279, 50277, 1, 0]
		for stop_id in stop_ids:
			if input_ids[0][-1] == stop_id:
				return True
		return False
            
@retry(stop_max_attempt_number=10)
@RateLimiter(max_calls=1200, period=60)
@backoff.on_exception(backoff.expo, (openai.error.RateLimitError,
                                     openai.error.ServiceUnavailableError,
									 openai.error.APIError))
def generate_response_fn(args, utt, persona=''):
	"""Use appropriate model to generate a response."""
	if args.model_type == 'blender':
		# V1: Use parlai framework
		args.model.reset()
		if persona.strip():
			utt = persona.strip() + '\n' + utt
		args.model.observe({'text': utt, 'episode_done': False})
		response = args.model.act()
		return response['text']
	
	elif args.model_type == 'alpaca':
		if persona.strip():
			input = '### Instruction: {} \n ### Input: {} \n ### Response:'.format(persona, utt)
			input_ids = args.tokenizer.encode(input)
		else:
			input_ids = args.tokenizer.encode(utt)
		input_id_len = len(input_ids)
		input_ids = torch.tensor(input_ids, device=args.device, dtype=torch.long).unsqueeze(0)
		out = args.model.generate(input_ids, max_new_tokens=60, repetition_penalty=1.0)[0]
		text = args.tokenizer.decode(out[input_id_len:], skip_special_tokens=True, clean_up_tokenization_spaces=False)
		
		if text.find(args.tokenizer.eos_token) > 0:
			text = text[:text.find(args.tokenizer.eos_token)]
		text = text.strip()
		if args.model_type == 'alpaca':
			print('Alpaca: {}'.format(text))
		return text
	
	elif args.model_type == 'vicuna':
		utt = persona + '\n' + utt
		input_ids = args.tokenizer.encode(utt)
		input_id_len = len(input_ids)
		input_ids = torch.tensor(input_ids, device=args.device, dtype=torch.long).unsqueeze(0)
		out = args.model.generate(input_ids, temperature=0.7, top_p=1.0, max_new_tokens=60, repetition_penalty=1.0)[0]
		text = args.tokenizer.decode(out[input_id_len:], skip_special_tokens=True, clean_up_tokenization_spaces=False)
		
		if text.find(args.tokenizer.eos_token) > 0:
			text = text[:text.find(args.tokenizer.eos_token)]
		text = text.strip()
		print('Vicuna: {}'.format(text))
		return text
		

def trim_text(text):
	"""Helper fn to cut off generated output at the first ./?/! if there is one."""
	end_punc = '.!?'
	min_end_idx = 1000
	for end in end_punc:
		end_idx = text.find(end)
		if 0 < end_idx < min_end_idx:
			min_end_idx = end_idx
	if min_end_idx == 1000:
		return text
	else:
		if min_end_idx + 2 < len(text) and text[min_end_idx + 1] == '"':
			return text[:min_end_idx + 2]
		else:
			return text[:min_end_idx + 1]
