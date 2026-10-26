# Chapter 2 · Let the AI read the reviews

Here's the fun part. Most review stacks on retail pages are honest but unreadable: fifty reviews of a dishwasher, all five paragraphs, all starting with "I bought this to replace...". You could read all of them. You have better things to do. An AI model can read them in seconds and hand you a summary.

But an unsupervised AI summary is exactly as trustworthy as an excited intern: fast, eager, and capable of confidently inventing things. So this chapter is a loop with three parts: **collect, summarize, verify**. The verify part is what keeps this from being voodoo.

## Step 1: Collect the raw material

Gather reviews the same way a careful researcher would:

- **Retailer reviews** for the specific model numbers on your shortlist. Include the middles: copy the 1-, 2-, and 3-star reviews too, not just the fawning ones.
- **Community forums** (the Reddit thread titled "[category] megathread" is usually gold) for long-term opinions: "after six months, here's what broke."
- **Expert reviews**, for measured facts like brightness, noise, and durability.

Copy them into a plain text file, one per line, pasted in full. While you copy, jot down **where** and **when** each batch came from; you'll need that for fact-checking.

Two privacy rules while you collect:

- Paste **products, not people**. Reviews and spec sheets are fine. Your own address, account numbers, and order history are not. Nothing you paste should include your real name or contact details.
- Trim the fat. Two hundred reviews is fine; two thousand is a prompt that costs more than it teaches. Twenty to sixty well-chosen reviews (heavily weighted toward the grumpy ones) is plenty.

## Step 2: The summarizing prompt

Now the prompt. The trick that makes AI summaries trustworthy is **constraining** them: tell the model exactly what it may and may not do. Here's the template this manual recommends:

```
I'm shopping for a {product}. Below are customer reviews copied
from a retailer page. Summarize them for a buyer:

1. The three most common complaints, with a count of how many
   reviews mention each.
2. The two most praised qualities, same deal with counts.
3. Reviews that seem fake, promotional, or copy-pasted from
   other reviews. List which ones and quote the offending text.

Rules for your answer:
- Quote exact sentences from the reviews when you claim
  anything. If you can't quote it, don't claim it.
- If something appears in only one review, say "one review
  only". Do not inflate it.
- Don't use any outside knowledge. Only what's below.

REVIEWS:
[paste reviews here]
```

Why these rules work: counting and quoting keep the model anchored to the actual text. Asking it to flag fake-looking reviews gives you a head start on [Chapter 3](spot-fakes.html) for free. And "no outside knowledge" stops it from decorating your summary with things it half-remembers from some other dishwasher.

## Step 3: Match the summary against YOUR criteria

A generic summary is nice; a summary filtered against your [criteria list from Chapter 1](criteria.html) is a decision tool:

```
Here are my must-have criteria for this purchase:
[your MUST list]

Based only on the reviews above, which of my MUST criteria are
supported, challenged, or not mentioned at all? Quote each
relevant review line. End with the sentence "No review evidence
about: [criteria that never came up]" if any criterion was
never touched on.
```

That last line matters. Criteria with **no review evidence** are your homework: those are the claims only the spec sheet (see [Chapter 4](spec-sheets.html)) or your own eyes can settle.

## Step 4: Verify (the part that isn't optional)

AI models make mistakes in a very specific, human-sounding way: they compress, they blur, and occasionally they just make things up while sounding completely certain. The term you'll hear is "hallucination." Three checks catch almost all of it:

1. **Spot-check the quotes.** Pick two quotes from the summary and search for the exact phrase in your collected reviews file. (Ctrl-F is your friend.) If the quote isn't there, your trust in the summary should be zero until it earns it back.
2. **Recheck the two or three biggest claims somewhere else.** "Battery dies fast" should show up in a second source: a forum, another retailer, a reviewer's measurements. One source is an anecdote; two are a pattern; three, reviewers with lab equipment.
3. **Send numbers to the official spec page.** Any claim like "it's 44 dB" or "it has 16 GB of RAM" gets checked against the manufacturer's spec sheet, never against reviews, and never against the AI's memory.

If a summary survives those three checks, you can lean on it. Write the survivors into [worksheet Step 4](worksheet.html) so the work outlives the chat session. Then un-trust it exactly one notch whenever the data changes (a new firmware update, a different model year), because AI summaries have a short shelf life.

> One more habit worth stealing: ask the model to say "I'm not sure" more often. A closing line like *if anything above is uncertain, flag it* costs nothing and surfaces a surprising number of shaky claims.

Next: [Chapter 3 · Fakes, shills, and affiliate funnels](spot-fakes.html)
