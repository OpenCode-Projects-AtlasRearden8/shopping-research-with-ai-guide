# Chapter 6 · Ask the model what you're missing

Every research process hits the same blind spot: it's brilliant at answering the questions you thought of, useless at the ones you didn't. You can't think of those yourself, by definition. But a model can, because AI systems have read a million purchase stories, including every flavor of "I wish someone had told me."

This chapter is a small toolkit of prompts for prying open that blind spot. Use them **before** the money moves. They take minutes and they've saved more purchases than any coupon ever will.

## The pre-mortem: assume it went wrong

A pre-mortem is an old planning trick: imagine the project failed, then work backwards to why. Applied to shopping:

```
I'm about to buy the following, for the following reasons.
Imagine one month has passed and I'm disappointed. Write the
six most likely reasons for my regret, ranked from most to
least likely, and be specific. Reference my criteria below;
tell me which of my MUSTs is most likely to quietly fail.

Product: {what and which model}
Why I'm buying it: {your reasons}
My MUST criteria: [paste from your worksheet]
```

What makes this pre-mortem work: it forces the model to argue against *you*, given your own words. Even when you disagree with its scenarios, running your eyes over them surfaces the risk you'd been avoiding. If you can't rebut a scenario, fix the plan or fix the criteria.

## The skeptical friend: steelman the alternatives

```
Here is my planned purchase and its price: {...}.

In three short arguments, convince me that:
(a) a cheaper alternative serves me just as well,
(b) a pricier alternative is actually the better buy,
(c) I shouldn't buy anything in this category at all,
    because some other approach solves my real problem.

For (c), describe my real-world goal in one sentence first.
```

Part (c) is the sleeper hit. Sometimes the honest answer to "best washing machine under $600" is "a 15-minute walk to the laundromat down the street," and the deal that saves you $600 is not buying the washer. This prompt is your polite, tireless expert: it argues every side with the same care, minus the sales associate's commission.

## The missing-questions prompt

```
I'm buying {product}. List ten questions I should be asking but
probably haven't thought of, from the perspective of:
- a repair technician who sees these come in weekly,
- a long-term owner two years down the line,
- someone who successfully returned theirs.

For each question, tell me where I'd find the answer
(spec sheet, review, warranty document, or trial period).
```

Notice the last line. The answer locations ("warranty document") point you to exactly the boring reading that prevents the famous regrets, the ones with fine print.

## The spec sheet autopsy

This one pairs with [Chapter 4](spec-sheets.html). Paste the full spec sheet of your favorite candidate:

```
Here is the full spec sheet for {model}.

1. Translate every line to plain English, one line each.
2. Flag any line that looks weak, hidden, or phrased to
   distract, and say why.
3. Identify the three lines that matter most for this use
   of mine: {your real use, from the worksheet}.

Don't recommend alternatives. Don't summarize my needs.
Only analyze the sheet.
```

The instruction "don't recommend alternatives" isn't fussiness: you'll get better analysis when the model isn't trying to close a sale. You've done the shortlisting; the model is your auditor, not your salesperson.

## The mirror prompt

Last one, and it might be the most valuable prompt in this whole manual:

```
Here is how I've described my planned purchase:
{paste your own words from this conversation}

Notice what I have NOT mentioned anywhere above. What underlying
want or worry am I probably trying to solve that I haven't said
out loud? Answer in two sentences.
```

Past you left clues in how you describe the purchase. "I want a great camera phone" might really mean "I miss taking photos like I used to." "A really nice mattress" might mean "I want to feel like someone is taking care of me, starting at midnight." A model asked this way will sometimes reflect your real want back at you, and your real want might cost $0, or a completely different purchase.

That reflection is also where this manual's whole method loops back: the [worksheet's final step](worksheet.html) asks for that honest sentence. When you can write it plainly, whether you buy or not, you'll know exactly why, and that's what "without regret" actually means.

The AI is a tool for seeing your own decision more clearly, not for making the decision for you. It's extra pairs of eyes, the friend who reads warranty documents for fun, the cold shower before the checkout button. Use it that way and you'll rarely regret either the purchase or the skip.

Previous: [Chapter 5 · When to buy](timing.html) · Then: the [before-you-buy worksheet](worksheet.html)
