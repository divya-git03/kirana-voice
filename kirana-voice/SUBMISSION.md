# Submission kit (copy-paste)

## Project title
Kirana Voice: Hinglish phone-order assistant for neighbourhood stores

## Problem
Kirana owners miss or mishear phone orders in code-mixed Hindi-English while serving customers at the counter.

## Who will use it
Kirana store owners and their regular customers (starting with Hindi/Hinglish speakers).

## Gnani AI models used
Prisma v3.0 (speech-to-text, indic-auto) and Timbre v2.5 (text-to-speech, Nalini, hi-IN).

## Contribution
Solo: everything (parser, API integration, server, noise benchmark, demo).

## 60-second demo script
0-8s   Hook: "Kirana stores run on phone calls. Here's one being answered by AI."
8-25s  Speak: "Bhaiya, do kilo chawal aur ek packet maggi." Show transcript (Prisma v3.0), then the spoken reply (Timbre v2.5): "2 kilo chawal, 1 packet Maggi, total 134 rupaye. Confirm karein?"
25-38s Add: "ek litre tel bhi." Basket updates to 294.
38-50s Say "haan theek hai." Order number is spoken.
50-60s Show the noisy 8 kHz benchmark table. Close with repo link.

## LinkedIn / X post
I built Kirana Voice 🛒📞 an AI that answers a kirana store's phone call, understands Hinglish orders ("do kilo chawal aur ek packet maggi"), and reads back the priced order.

Built on @Gnani.ai Prisma v3.0 (speech-to-text) + Timbre v2.5 (text-to-speech), and tested on noisy 8 kHz telephony audio.

Code: https://github.com/divya-git03/kirana-voice

#GnaniAI #GreatIndianAIInternshipChallenge
