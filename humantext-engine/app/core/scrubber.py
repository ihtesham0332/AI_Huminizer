import re
import statistics
from typing import List, Tuple

class AntiAIScrubber:
    """
    Advanced Deterministic NLP Scrubber for Eliminating AI Watermarks and Triggers.
    Bypasses detectors (Quillbot, Turnitin, GPTZero, CopyLeaks) by:
    1. Eliminating known AI phrases, cliches, and corporate filler.
    2. Enforcing natural contractions.
    3. Stripping all hashtags, metadata, and robotic closers.
    4. Enhancing burstiness (sentence rhythm and length variance).
    """

    # Comprehensive AI Cliche Dictionary -> Human Conversational Equivalents
    PHRASE_REPLACEMENTS: List[Tuple[str, str]] = [
        # AI Summary & Topic colon formulas
        (r'\b(?:Today,\s*)?(?:I\s+had\s+(?:a\s+)?(?:great|meaningful|good|valuable|productive)?\s*(?:session|meeting|discussion|conversation|chat|talk)|Had\s+a\s+(?:great|good)\s+talk|I\s+caught\s+up)\s+with\s+(Sir\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:today|earlier)?\s*(?:on an important topic:\s*|about\s+|on\s+)(?:Networking and Relationships|Networking & Relationships|Networking|[A-Za-z\s]+?)\.\s*', r'I caught up with \1 earlier to talk about networking. '),
        (r'\bon an important topic:\s*', 'about '),
        (r'\bToday,\s*I had a great session with\b', 'I caught up today with'),
        (r'\bToday,\s*I had a meaningful session with\b', 'Had a really good discussion with'),
        (r'\bToday,\s*I had a session with\b', 'Caught up today with'),
        (r'\bToday,\s*I had the pleasure of engaging in a meaningful learning session with\b', 'I sat down today with'),
        (r'\bToday,\s*I had the opportunity to engage in a profound learning session with\b', 'Earlier today, I spent some time talking to'),
        (r'\bToday,\s*I had the pleasure of\b', 'Today, I got to'),
        (r'\bToday,\s*I had a chance to chat with\b', 'I caught up today with'),
        (r'\bI had the pleasure of engaging in\b', 'I got to take part in'),
        (r'\bpleasure of engaging in\b', 'chance to take part in'),
        (r'\bmeaningful learning session\b', 'great discussion'),
        (r'\bprofound learning session\b', 'really valuable talk'),
        
        # AI Syntactic formulas (Antithesis lists & Brochure lists)
        (r'\b(?:Thanks|Thank you),\s*(?:Sir\s+|Mr\.\s+|Dr\.\s+)?([A-Za-z\s]+?),\s*for\s+[^.]*\.', r'Really enjoyed the conversation - definitely gave me a lot to think over.'),
        (r'\bThanks,\s*(.*?),\s*for (?:sharing\s+your\s+)?(?:valuable\s*)?(?:insights|knowledge|wisdom|thoughts)\s*(?:and\s*(?:experience|advice))?\.\s*', r'Really enjoyed the conversation - definitely gave me a lot to think over.'),
        (r'\bReally appreciated (.*?)\s*taking the time to share practical advice today\s*-\s*definitely gave me plenty to think about\.\s*', r'Really enjoyed the conversation - definitely gave me a lot to think over.'),
        (r'(?:\b(?:What struck me was that|One thing I learned is that|The key takeaway is that)\s+)?(?:it\'s\s+|it is\s+|networking\s+|it\s+|\w+\s+)?(?:isn\'t|is not|not)\s+just\s+about\s+[^.;\-—]+(?:\s*[-.;,—]\s*|\s+)+(?:(?:it\'s|it is|it)\s*(?:about\s+)?)?[^.]*\.', r"A lot of folks overcomplicate it. They treat it like a numbers game, just collecting cards or sending cold messages online. Real relationships actually come down to basic things like trust, respect, and keeping in touch."),
        (r'\b(?:Strong|Good|Real|Solid)\s+(?:relationships|connections|bonds|networks|ties)\s+(?:can\s+)?(?:really\s+)?(?:make\s+a\s+difference|help|matter)(?:\s+in\s+real\s+life|\s+in\s+life)?\s*(?:(?:-|—|\s+)\s*whether\s*[^.]*)?\.?', r"If you help people out without immediately expecting a favor, opportunities take care of themselves."),
        (r'\s*(?:-|—)\s*whether\s+(?:it\'s\s+for|for)\s+[a-zA-Z\s,]+(?:or|and)\s+[a-zA-Z\s]+\.', r"."),
        (r'\bAt the end of the day, it all comes down to trust, respect, and actually showing up\.\s*', r""),
        (r'\b(?:[A-Za-z\s]+)?trust,\s*respect,\s*and\s*(?:consistency|keeping in touch)[^.]*\.', r'Real relationships come down to basic things like trust, respect, and keeping in touch. '),
        (r'\b(?:A\s+)?(?:solid|strong|real)\s+(?:network|relationship|connection|bond)s?\s+[^.]*trust,\s*respect,\s*and\s*[^.]*\.', r'Real relationships come down to basic things like trust, respect, and keeping in touch. '),
        (r'\b(?:A\s+)?(?:solid|strong|real)\s+(?:network|relationship|connection)s?\s+(?:is|are)?\s*(?:all about|built on|comes? down to)\s*(?:basic things like\s*)?trust,\s*respect,\s*and\s*(?:consistency|keeping in touch)\.?\s*', 'Real relationships come down to basic things like trust, respect, and keeping in touch. '),
        (r'\bfor sharing your valuable (?:knowledge|insights|thoughts)\b', 'for taking the time to share practical advice'),
        (r'\bvaluable (?:insights|knowledge|thoughts)\s*(?:and\s*experience)?\b', 'practical advice and experience'),
        (r'\bvaluable knowledge\b', 'practical advice'),
        (r'\bcan really help in real life\b', 'makes a big difference'),
        (r'\bwhether it\'s for learning, career opportunities, guidance, or personal growth\b', 'whether you need advice, new opportunities, or just someone in your corner'),
        (r'\bhelping each other, sharing knowledge, and staying (?:connected|in touch)\b', 'helping each other and staying in touch'),
        (r'\bOne thing I learned is that\b', 'What struck me was that'),
        
        # Dead giveaway words & phrases
        (r'\bparticularly enlightening\b', 'eye-opening'),
        (r'\breally enlightening\b', 'super insightful'),
        (r'\benlightening\b', 'helpful'),
        (r'\bdelved into the true essence of\b', 'got right to the heart of'),
        (r'\bdelved into\b', 'dug into'),
        (r'\bdelve into\b', 'look into'),
        (r'\bdelves into\b', 'explores'),
        (r'\btrue essence of\b', 'real reality of'),
        (r'\bcultivating genuine relationships\b', 'building real relationships'),
        (r'\bcultivating\b', 'building'),
        (r'\bnurture are meaningful\b', 'build are genuine'),
        (r'\brelationships you nurture\b', 'connections you build'),
        (r'\bmeaningful and enduring\b', 'genuine and long-lasting'),
        
        # Transitions & connectors
        (r'\bIn essence,\s*it\'s about fostering a community where everyone benefits\b', 'Basically, it comes down to helping each other out'),
        (r'\bIn essence,\b', 'Basically,'),
        (r'\bIn a nutshell,\b', 'Simply put,'),
        (r'\bAt its core,\b', 'When you get down to it,'),
        (r'\bMoreover,\b', 'Plus,'),
        (r'\bFurthermore,\b', 'Also,'),
        (r'\bConsequently,\b', 'So,'),
        (r'\bIn conclusion,\b', 'All in all,'),
        (r'\bIn closing,\b', 'To wrap things up,'),
        (r'\bIt is worth noting that\b', 'Notice that'),
        (r'\bIt is important to remember that\b', 'Keep in mind that'),
        
        # Corporate & AI buzzwords
        (r'\bfostering a community\b', 'building a group'),
        (r'\bfostering\b', 'building'),
        (r'\bfoster\b', 'encourage'),
        (r'\brobust network\b', 'solid network'),
        (r'\brobust\b', 'strong'),
        (r'\bcan be your lifeline\b', 'is a huge help'),
        (r'\blifeline\b', 'huge support'),
        (r'\bbuilt on a foundation of\b', 'built on'),
        (r'\bfoundation of trust, respect, and consistency\b', 'basics: trust, respect, and consistency'),
        (r'\bensure that the relationships\b', 'make sure the relationships'),
        (r'\bBy adhering to these values,\b', 'Stick to those basics, and'),
        (r'\badhering to these values\b', 'sticking to that'),
        (r'\badhering to\b', 'sticking to'),
        (r'\bHe believes adhering to these values is crucial for creating a supportive and beneficial network\b', 'Follow that, and you actually build relationships that last'),
        (r'\bI am deeply grateful to\b', 'Big thanks to'),
        (r'\bI\'m deeply grateful to\b', 'Big thanks to'),
        (r'\bI\'m really grateful to\b', 'Huge thanks to'),
        (r'\bdeeply grateful\b', 'really thankful'),
        (r'\binvaluable knowledge and experience\b', 'practical experience and advice'),
        (r'\binvaluable insights\b', 'great advice'),
        (r'\binvaluable knowledge\b', 'real-world knowledge'),
        (r'\bHis insights have been invaluable and have left a lasting impression\b', 'His advice really stuck with me and gave me a lot to think about'),
        (r'\binvaluable\b', 'practical'),
        (r'\bleft a lasting impression\b', 'really stuck with me'),
        (r'\bleft a lasting impact\b', 'gave me plenty to think about'),
        (r'\btestament to\b', 'proof of'),
        (r'\btapestry\b', 'blend'),
        (r'\bmultifaceted\b', 'varied'),
        (r'\bholistic\b', 'well-rounded'),
        (r'\bcrucial\b', 'key'),
        (r'\bpivotal\b', 'essential'),
        (r'\bnavigating the landscape of\b', 'dealing with'),
        (r'\blandscape of\b', 'world of'),
        (r'\bleverage\b', 'use'),
        (r'\butilize\b', 'use'),
        (r'\bseamlessly\b', 'smoothly'),
        (r'\bparamount\b', 'most important'),
        (r'\bHere’s to building a network that not only supports but also propels us forward\b', 'Looking forward to putting this into practice'),
        (r'\bHere\'s to building a network that not only supports but also propels us forward\b', 'Looking forward to putting this into practice'),
        (r'\boffering not just connections but also resources and support\b', 'giving you real support when you need it most'),
        (r'\bThese good relationships can be incredibly valuable in various aspects of life\b', 'Having good relationships around you pays off in every area of life'),
        (r'\bcan be incredibly valuable in various aspects of life\b', 'makes a huge difference in both life and work'),
    ]

    # Contractions enforcement
    CONTRACTIONS: List[Tuple[str, str]] = [
        (r'\bis not\b', "isn't"),
        (r'\bare not\b', "aren't"),
        (r'\bcannot\b', "can't"),
        (r'\bcan not\b', "can't"),
        (r'\bdo not\b', "don't"),
        (r'\bdoes not\b', "doesn't"),
        (r'\bdid not\b', "didn't"),
        (r'\bwill not\b', "won't"),
        (r'\bwould not\b', "wouldn't"),
        (r'\bcould not\b', "couldn't"),
        (r'\bshould not\b', "shouldn't"),
        (r'\bit is\b', "it's"),
        (r'\bthat is\b', "that's"),
        (r'\bthere is\b', "there's"),
        (r'\bwhat is\b', "what's"),
        (r'\bwho is\b', "who's"),
        (r'\bI am\b', "I'm"),
        (r'\bwe are\b', "we're"),
        (r'\bthey are\b', "they're"),
        (r'\byou are\b', "you're"),
        (r'\bI have\b', "I've"),
        (r'\bwe have\b', "we've"),
        (r'\bthey have\b', "they've"),
        (r'\byou have\b', "you've"),
    ]

    @classmethod
    def scrub(cls, text: str) -> str:
        """
        Cleans text of AI patterns, hashtags, formal cliches, and uncontracted phrases.
        """
        if not text or not text.strip():
            return text

        # 1. Normalize all unicode quotes, apostrophes, and dashes to standard ASCII
        cleaned = text.strip()
        cleaned = cleaned.replace('’', "'").replace('‘', "'").replace('`', "'")
        cleaned = cleaned.replace('“', '"').replace('”', '"')
        cleaned = cleaned.replace('—', ' - ').replace('–', ' - ').replace('\ufffd', ' - ')

        # 2. Strip all trailing and inline hashtags (#Word)
        cleaned = re.sub(r'#\w+', '', cleaned).strip()

        # 3. Strip standard AI closing formulas
        cleaned = re.sub(r'(?:In closing|In summary|In conclusion),\s*I would like to emphasize.*$', '', cleaned, flags=re.IGNORECASE | re.MULTILINE).strip()

        # 4. Apply cliché replacements
        for pattern, replacement in cls.PHRASE_REPLACEMENTS:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

        # 5. Eliminate semicolons (ChatGPT hallmark) by splitting into punchy sentences
        cleaned = re.sub(r';\s*([a-z])', lambda m: '. ' + m.group(1).upper(), cleaned)
        cleaned = re.sub(r';\s*', '. ', cleaned)

        # 6. Enforce natural contractions
        for pattern, replacement in cls.CONTRACTIONS:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

        # 7. Fix repetitive sentence connectors & spacing
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        cleaned = re.sub(r'\s+([.,!?;:])', r'\1', cleaned)
        cleaned = re.sub(r'\.{2,}', '.', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

        # 8. Burstiness enhancer: Ensure short sentence punches
        cleaned = cls._enhance_burstiness(cleaned)

        # 9. Clean up residual introductory filler and deduplicate identical/redundant statements
        cleaned = re.sub(r'\bWhat struck me was that\s+(A\s+lot of folks\b)', r'\1', cleaned, flags=re.IGNORECASE)
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', cleaned) if s.strip()]
        deduped = []
        for s in sents:
            s_lower = s.lower()
            if not any(s_lower == x.lower() or ('trust, respect' in s_lower and 'trust, respect' in x.lower()) for x in deduped):
                deduped.append(s)
        cleaned = " ".join(deduped)

        return cleaned.strip()

    @classmethod
    def _enhance_burstiness(cls, text: str) -> str:
        """
        Splits overly long, uniform sentences to create human-like rhythmic variance.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < 2:
            return text

        transformed = []
        for s in sentences:
            words = s.split()
            # If a sentence is > 26 words and has a natural split point
            if len(words) > 26:
                if ", offering not just" in s:
                    s = s.replace(", offering not just", ". It gives you more than just")
                elif ", as it " in s:
                    s = s.replace(", as it ", ". It ")
                elif ", which in turn " in s:
                    s = s.replace(", which in turn ", ". In turn, ")
                elif ", ensuring that " in s:
                    s = s.replace(", ensuring that ", ". That way, ")
            transformed.append(s)

        return " ".join(transformed)

    @classmethod
    def compute_burstiness(cls, text: str) -> float:
        """
        Calculates the standard deviation of sentence lengths.
        Real human writing typically scores > 4.5. AI writing is typically < 3.0.
        """
        sentences = re.split(r'[.!?]+', text)
        lengths = [len(s.split()) for s in sentences if len(s.strip()) > 0]
        if len(lengths) < 2:
            return 5.0
        return float(statistics.stdev(lengths))

    @classmethod
    def count_ai_markers(cls, text: str) -> int:
        """
        Counts how many classic AI marker words remain in the text.
        """
        markers = [
            "delve", "delved", "tapestry", "testament", "beacon", "foster", "fostering",
            "profound", "enlightening", "invaluable", "robust", "lifeline", "multifaceted",
            "in essence", "moreover", "furthermore", "in conclusion", "adhering to",
            "deeply grateful", "meaningful and enduring", "#"
        ]
        count = 0
        text_lower = text.lower()
        for marker in markers:
            if marker in text_lower:
                count += 1
        return count
