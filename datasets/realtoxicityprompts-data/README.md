# RealToxicityPrompts Data
The RealToxicityPrompts is a corpus of English prompts (specifically sentence beginnings) of varying toxicity. These prompts are meant to be given as contexts to an autoregressive language model (ie. GPT-2) and used for generating completions. More details are presented in our [paper](https://api.semanticscholar.org/CorpusID:221878771).

We've also included metadata and generations as described in the paper.

## File Formats
All data is released in the [JSON Lines](https://jsonlines.org/) (`.jsonl`) format.

## Toxicity Score Attributes
The following are the the toxicity attributes we provide for each piece of text, as returned by the [Perspective API](https://www.perspectiveapi.com/):
- toxicity
- severe\_toxicity
- profanity
- sexually\_explicit
- identity\_attack
- flirtation
- threat
- insult

More information can be found in the [Pespective API model documentation](https://github.com/conversationai/perspectiveapi/blob/master/2-api/models.md).

## Contents
Note: we will denote the following schema as *text and toxicity*:
- text
- toxicity
- severe\_toxicity
- profanity
- sexually\_explicit
- identity\_attack
- flirtation
- threat
- insult

- `prompts.jsonl`: contains prompts and associated metadata
    - filename, begin, end: filename and character begin/end in OWTC that the prompt was taken from
    - challenging: whether the prompt challenges all out-of-the-box models, as described in the paper
    - prompt: *text and toxicity* for the prompt (the first half of the sentence)
    - continuation: *text and toxicity* for the continuation (the remainder of the sentence)
- `generations`:
    - `eos`: contains a `.jsonl` file for each model, each containing containing *text and toxicity* for EOS-prompted generations
    - `prompted`: contains a `.jsonl` file for each model, each containing a superset of the `prompts.jsonl` file with an additional `generations` column which contains arrays of generation *text and toxicity*
- `metadata`:
    - `media_bias_fact_check.jsonl`: contains factual reliability (`fact`) and political bias (`bias`) for a set of domains. For more information, see the repository for [Factuality and Bias Prediction of News Media](https://github.com/ramybaly/News-Media-Reliability).
    - `openwebtext_meta.jsonl`: contains metadata for [OpenWebTextCorpus](https://skylion007.github.io/OpenWebTextCorpus/).
    - `reddit_banned_subreddits.jsonl`: contains a list of banned subreddits along with the ban reason, as collected from the `r/reclassified` subreddit.
    - `reddit_subscriber_counts.jsonl`: contains the number of subscribers for a number of subreddits

