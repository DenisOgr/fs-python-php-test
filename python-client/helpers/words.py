from faker.providers import BaseProvider
import json
import random

class DictProvider(BaseProvider):

    raw_data = '["future", "thus", "start", "good", "great", "majority", "up", "expert", "those", "head", "technology", "old", "half", "feeling", "expect", "chair", "traditional", "air", "available", "politics", "discover", "base", "check", "operation", "future", "decade", "brother", "opportunity", "PM", "may", "effect", "color", "usually", "public", "organization", "think", "bad", "me", "employee", "account", "how", "sea", "film", "project", "maintain", "often", "worry", "send", "clearly", "ok", "federal", "shake", "finish", "society", "notice", "until", "thought", "always", "although", "rock", "forward", "meet", "mouth", "who", "foreign", "field", "yourself", "area", "morning", "need", "role", "fight", "sing", "move", "series", "health", "there", "among", "network", "relate", "figure", "so", "family", "later", "statement", "media", "nice", "blood", "hundred", "least", "physical", "everyone", "contain", "four", "institution", "that", "some", "more", "fine", "agree", "much", "difficult", "today", "clear", "way", "recognize", "two", "wonder", "now", "site", "American", "drive", "series", "anything", "on", "safe", "life", "quickly", "how", "laugh", "foreign", "focus", "TV", "later", "specific", "write", "hand", "send", "administration", "including", "quickly", "itself", "people", "mission", "treat", "well", "north", "level", "practice", "wait", "develop", "somebody", "need", "can", "former", "realize", "college", "sport", "report", "new", "nothing", "deal", "table", "pretty", "maybe", "institution", "around", "exactly", "that", "draw", "ago", "collection", "issue", "take", "space", "store", "window", "education", "experience", "save", "finally", "happy", "soldier", "then", "marriage", "even", "visit", "country", "environmental", "fish", "personal", "hair", "simple", "interview", "first", "or", "continue", "know", "read", "federal", "home", "always", "bag", "defense", "you", "meeting", "push", "who", "party", "forget", "several", "put", "current", "serious", "stand", "themselves", "treat", "would", "hold", "hit", "series", "throughout", "accept", "home", "various", "choose", "democratic", "may", "Mr", "art", "or", "black", "language", "yes", "son", "per", "guy", "reason", "appear", "skill", "spend", "well", "word", "store", "tax", "down", "how", "relate", "wear", "find", "choice", "better", "suddenly", "notice", "whether", "enough", "throw", "room", "to", "apply", "know", "product", "Mr", "hot", "sing", "media", "house", "produce", "color", "social", "city", "wall", "response", "body", "successful", "learn", "modern", "population", "policy", "throw", "trade", "couple", "news", "enter", "red", "eye", "girl", "response", "individual", "yeah", "defense", "believe", "fear", "own", "establish", "involve", "anything", "team", "let", "situation", "way", "about", "research", "mother", "federal", "product", "job", "prepare", "radio", "measure", "bank", "require", "even", "modern", "look", "reflect", "old", "traditional", "contain", "camera", "now", "popular", "traditional", "adult", "real", "because", "name", "information", "and", "parent", "science", "home", "better", "customer", "over", "spend", "across", "let", "write", "view", "cover", "small", "PM", "entire", "present", "color", "become", "during", "officer", "red", "truth", "federal", "cost", "leave", "west", "career", "southern", "left", "event", "rest", "hope", "outside", "sell", "trial", "player", "be", "leg", "issue", "form", "issue", "current", "worker", "production", "note", "market", "thank", "project", "doctor", "wind", "either", "send", "these", "history", "official", "detail", "Congress", "name", "I", "check", "field", "little", "anyone", "young", "produce", "this", "significant", "however", "value", "soldier", "pretty", "north", "around", "imagine", "plan", "gun", "defense", "might", "song", "reality", "structure", "positive", "side", "share", "analysis", "might", "since", "large", "low", "these", "stock", "economy", "your", "middle", "thousand", "method", "pressure", "nearly", "agree", "kid", "modern", "quite", "Mrs", "break", "language", "Democrat", "report", "television", "know", "win", "development", "American", "program", "minute", "together", "keep", "actually", "color", "house", "now", "pattern", "now", "hear", "reason", "glass", "list", "century", "kid", "call", "get", "down", "rule", "value", "walk", "remember", "detail", "create", "window", "see", "believe", "blood", "produce", "sport", "spend", "other", "including", "international", "day", "wait", "boy", "agree", "Republican", "radio", "safe", "scientist", "move", "quickly", "store", "election", "continue", "data", "effort", "hope", "recent", "age", "not", "write", "case", "indeed", "yet", "reach", "onto", "capital", "most", "range", "recognize", "course", "piece", "environment", "himself", "head", "form", "serve", "where", "conference", "through", "everyone", "front", "feeling", "growth", "despite", "country", "which", "source", "quickly", "without", "state", "action", "that", "relationship", "thing", "action", "experience", "any", "which", "adult", "fall", "hour", "several", "position", "red", "up", "crime", "improve", "thank", "capital", "seem", "other", "cultural", "up", "successful", "program", "street", "factor", "partner", "whose", "stage", "rather", "as", "mention", "win", "play", "note", "west", "law", "seat", "campaign", "something", "go", "walk", "hospital", "draw", "rest", "other", "record", "use", "involve", "sea", "power", "lead", "example", "friend", "along", "fight", "home", "little", "know", "everything", "car", "western", "mouth", "not", "nor", "cup", "people", "similar", "data", "law", "professor", "able", "table", "contain", "partner", "see", "loss", "style", "until", "note", "clear", "product", "interest", "speech", "animal", "religious", "suddenly", "research", "wind", "reason", "rise", "federal", "on", "quality", "task", "play", "ahead", "other", "this", "environmental", "cost", "road", "traditional", "loss", "stock", "son", "economy", "decade", "consumer", "term", "director", "ten", "side", "end", "picture", "seek", "common", "spring", "name", "we", "right", "coach", "house", "order", "politics", "agent", "six", "special", "need", "watch", "seat", "less", "picture", "director", "war", "wife", "else", "draw", "can", "bar", "result", "girl", "price", "cup", "lose", "white", "enjoy", "only", "impact", "fast", "play", "eight", "yet", "far", "try", "training", "practice", "investment", "stop", "member", "green", "still", "statement", "performance", "middle", "section", "artist", "produce", "technology", "charge", "former", "size", "region", "nature", "concern", "big", "direction", "financial", "I", "fund", "thousand", "leave", "street", "official", "art", "four", "answer", "apply", "shake", "seek", "performance", "wall", "energy", "cause", "become", "moment", "here", "security", "great", "set", "others", "bag", "travel", "notice", "chance", "nation", "pull", "building", "floor", "successful", "type", "drop", "director", "make", "sense", "safe", "wind", "standard", "food", "game", "various", "million", "section", "speech", "box", "significant", "break", "family", "indeed", "clear", "commercial", "national", "lawyer", "consumer", "mission", "stuff", "establish", "care", "level", "performance", "play", "try", "move", "every", "act", "clear", "concern", "Mrs", "speech", "five", "find", "data", "challenge", "test", "which", "claim", "good", "small", "parent", "fine", "tax", "blood", "education", "event", "process", "happen", "be", "sure", "officer", "represent", "impact", "have", "sort", "personal", "feel", "push", "them", "together", "measure", "sing", "price", "product", "industry", "hotel", "process", "truth", "mean", "memory", "investment", "partner", "forget", "too", "place", "local", "policy", "morning", "race", "theory", "many", "few", "owner", "property", "movie", "white", "develop", "very", "production", "government", "second", "phone", "account", "research", "majority", "stand", "ready", "deep", "sit", "history", "road", "we", "wait", "reach", "senior", "economic", "voice", "spend", "free", "several", "listen", "president", "garden", "interesting", "marriage", "wonder", "rest", "similar", "reveal", "right", "pull", "debate", "must", "American", "among", "trial", "budget", "suddenly", "arm", "night", "service", "which", "offer", "yes", "kind", "window", "several", "thousand", "beyond", "bit", "control", "air", "pay", "alone", "there", "teacher", "have", "campaign", "break", "maintain", "tax", "among", "democratic", "participant", "present", "relate", "worry", "my", "maintain", "whom", "then", "peace", "anything", "believe", "high", "majority", "ground", "imagine", "family", "data", "term", "concern", "service", "population", "everyone", "civil", "million", "author", "cause", "walk", "great", "myself", "cup", "region", "media", "no", "front", "ever", "even", "true", "writer", "say", "about", "again", "tend", "forget", "building", "feeling", "require", "note", "heavy", "alone", "forward", "here", "table", "sell", "mention", "scientist", "hard", "fear", "white", "official", "under", "inside", "large", "fear", "often", "as", "record", "raise", "prevent", "best", "much", "if", "visit", "keep", "voice", "present", "entire", "night", "sometimes", "machine", "wish", "image", "federal", "vote", "writer", "away", "sea", "protect", "white", "paper", "early", "window", "investment", "production", "future", "several", "table", "myself", "even", "far", "practice", "later", "green", "relate", "if", "paper", "plant", "base", "believe", "doctor", "animal", "worker", "ever", "section", "board", "mind", "economy", "professional", "exist", "nothing", "yourself", "before", "now", "meeting", "between", "radio", "low", "provide", "model", "why", "six", "year", "court", "push", "part", "address", "rule", "agree", "science", "cold", "close", "try", "return", "fear", "decide", "project", "indicate", "alone", "difficult", "past", "skill", "team", "worry", "indicate", "walk", "strong", "action", "article", "before", "now", "government", "present", "unit", "perhaps", "line", "positive", "ten", "office", "today", "cultural", "husband", "receive", "picture", "whatever", "well", "near", "also", "exist", "seem", "face", "program", "certainly", "today", "ask", "concern", "hair", "suggest", "computer", "very", "piece", "protect", "change", "PM", "try", "what", "travel", "eight", "professional", "watch", "final", "partner", "best", "official", "industry", "occur", "tough", "however", "if", "where", "because", "stage", "pass", "check", "trial", "religious", "window", "or", "know", "understand", "white", "politics", "study", "eat", "kitchen", "send", "teach", "prove", "control", "painting", "tax", "single", "report", "course", "yard", "together", "whose", "too", "huge", "skin", "always", "third", "pattern", "chair", "become", "trade", "evening", "there", "thought", "beat", "religious", "entire", "sort", "stock", "worker", "first", "federal", "care", "sing", "key", "case", "serve", "enter", "open", "suddenly", "hotel", "want", "ten", "behavior", "dark", "should", "serve", "PM", "improve", "authority", "decision", "between", "their", "industry", "me", "white", "station", "table", "sometimes", "scientist", "find", "exactly", "admit", "read", "help", "must", "morning", "fund", "image", "name", "record", "coach", "then", "ahead", "stay", "get", "population", "space", "black", "site", "PM", "writer", "from", "big", "performance", "themselves", "guy", "science", "voice", "central", "factor", "size", "growth", "economic", "song", "avoid", "human", "increase", "sport", "prepare", "discover", "story", "property", "discover", "ago", "while", "staff", "onto", "note", "simple", "experience", "talk", "may", "view", "science", "serious", "team", "small", "almost", "whatever", "effort", "also", "prove", "number", "practice", "east", "hear", "great", "well", "financial", "material", "maintain", "situation", "factor", "movie", "arm", "strong", "church", "tree", "behavior", "respond", "may", "run", "this", "American", "realize", "ball", "present", "mother", "visit", "dark", "Congress", "again", "behavior", "debate", "edge", "cause", "news", "table", "might", "thank", "sense", "doctor", "word", "beat", "unit", "over", "great", "score", "material", "current", "fast", "over", "well", "weight", "leave", "behind", "own", "what", "him", "until", "treat", "sign", "account", "ground", "food", "serve", "prepare", "which", "bed", "wait", "quickly", "Republican", "case", "cell", "may", "policy", "data", "leader", "tax", "how", "born", "next", "discussion", "fine", "specific", "end", "perhaps", "billion", "remain", "ready", "since", "industry", "sing", "road", "each", "during", "Mr", "will", "institution", "clear", "bad", "what", "always", "necessary", "picture", "may", "stage", "enough", "surface", "understand", "building", "information", "child", "inside", "current", "room", "well", "subject", "feel", "conference", "technology", "research", "go", "step", "money", "then", "purpose", "past", "concern", "maybe", "although", "green", "note", "challenge", "economy", "serve", "floor", "finally", "analysis", "street", "analysis", "happy", "his", "scene", "day", "forget", "in", "Democrat", "bit", "day", "like", "coach", "week", "control", "bar", "region", "soon", "main", "career", "program", "discover", "game", "religious", "fine", "budget", "trial", "religious", "candidate", "upon", "control", "wind", "second", "more", "face", "myself", "information", "instead", "ability", "school", "forward", "number", "sometimes", "discover", "wide", "ask", "purpose", "with", "health", "condition", "race", "position", "draw", "data", "gun", "none", "positive", "fall", "wife", "determine", "ever", "thought", "hundred", "son", "understand", "sing", "that", "want", "require", "account", "young", "pressure", "experience", "daughter", "smile", "some", "start", "check", "magazine", "feel", "matter", "today", "might", "source", "apply", "letter", "weight", "think", "on", "response", "rule", "meet", "exist", "politics", "idea", "level", "team", "whole", "herself", "still", "see", "bar", "record", "as", "reach", "Mr", "must", "listen", "husband", "coach", "talk", "suddenly", "member", "possible", "teacher", "purpose", "interest", "item", "only", "pull", "care", "reach", "since", "investment", "suddenly", "turn", "success", "provide", "teach", "capital", "health", "entire", "early", "occur", "score", "off", "this", "serious", "administration", "authority", "choice", "owner", "others", "change", "hope", "early", "hour", "charge", "them", "feel", "southern", "suddenly", "that", "upon", "bit", "hair", "on", "address", "mouth", "story", "camera", "federal", "Democrat", "who", "administration", "firm", "billion", "visit", "step", "attorney", "begin", "kitchen", "cause", "concern", "because", "resource", "pretty", "Congress", "cut", "city", "arrive", "statement", "place", "old", "serve", "hear", "five", "east", "away", "discussion", "past", "lot", "face", "operation", "join", "American", "born", "certain", "example", "area", "already", "environmental", "while", "name", "case", "than", "meet", "catch", "bar", "list", "consumer", "whom", "successful", "black", "close", "local", "buy", "sure", "support", "street", "cut", "than", "hope", "man", "modern", "establish", "every", "week", "cold", "sign", "happy", "factor", "consumer", "throw", "item", "leader", "easy", "will", "behavior", "local", "tough", "behind", "here", "head", "federal", "body", "apply", "brother", "those", "try", "name", "child", "standard", "true", "recognize", "condition", "meeting", "which", "when", "finally", "your", "time", "wrong", "serve", "player", "daughter", "style", "coach", "sell", "generation", "be", "ready", "human", "really", "author", "require", "each", "several", "food", "rock", "nice", "choice", "baby", "evening", "international", "scene", "just", "property", "country", "forget", "actually", "discuss", "morning", "leave", "ok", "traditional", "culture", "deep", "available", "fly", "safe", "skin", "be", "skin", "raise", "around", "only", "effect", "line", "third", "safe", "develop", "unit", "teacher", "history", "feel", "main", "eye", "employee", "quality", "tend", "spend", "measure", "others", "on", "he", "project", "rate", "us", "maintain", "education", "throw", "see", "behind", "for", "political", "red", "course", "study", "something", "with", "west", "any", "street", "hope", "health", "risk", "and", "minute", "nor", "center", "far", "always", "career", "forget", "can", "ability", "player", "until", "food", "economic", "else", "weight", "rather", "bed", "whose", "general", "executive", "sort", "officer", "treatment", "could", "whose", "write", "he", "among", "piece", "quickly", "wind", "once", "coach", "particular", "allow", "good", "common", "activity", "age", "from", "war", "benefit", "stock", "drug", "fire", "story", "law", "live", "risk", "treat", "structure", "strategy", "maybe", "memory", "too", "simple", "eat", "general", "without", "car", "company", "listen", "reveal", "movement", "new", "child", "environment", "rule", "treatment", "admit", "increase", "safe", "them", "door", "three", "practice", "local", "himself", "develop", "growth", "partner", "sport", "information", "radio", "prevent", "life", "serve", "western", "own", "technology", "create", "instead", "almost", "scene", "dinner", "brother", "those", "law", "professional", "weight", "become", "cover", "edge", "represent", "general", "three", "worry", "say", "according", "economic", "fill", "here", "rather", "financial", "factor", "officer", "low", "article", "fight", "whole", "either", "drug", "population", "write", "event", "difficult", "film", "everything", "who", "century", "fill", "thus", "analysis", "weight", "consumer", "spring", "effect", "compare", "likely", "medical", "back", "work", "few", "much", "senior", "maybe", "unit", "way", "series", "write", "debate", "per", "generation", "brother", "three", "whole", "throw", "can", "human", "prove", "senior", "mouth", "most", "evidence", "those", "walk", "opportunity", "last", "project", "trade", "anything", "up", "international", "fine", "share", "quality", "clear", "body", "during", "experience", "color", "speak", "deal", "at", "scientist", "owner", "design", "blue", "score", "know", "enough", "listen", "build", "leader", "major", "guess", "there", "energy", "red", "its", "beautiful", "show", "force", "coach", "senior", "degree", "four", "onto", "our", "lay", "process", "because", "get", "number", "price", "computer", "evening", "different", "record", "present", "they", "behind", "argue", "structure", "this", "middle", "personal", "risk", "people", "light", "other", "moment", "me", "require", "article", "audience", "again", "we", "letter", "discussion", "car", "only", "red", "record", "give", "stage", "few", "focus", "yeah", "four", "effort", "talk", "TV", "church", "strong", "western", "call", "hospital", "course", "price", "work", "perhaps", "out", "under", "interest", "step", "local", "answer", "thing", "letter", "future", "improve", "assume", "despite", "hot", "past", "rather", "eye", "short", "recognize", "example"]'
    data = []
    def get_data(self):
        if not self.data:
            self.data = set(json.loads(self.raw_data))
        return self.data

    def seed_fake_words(self, number_of_words=1):
        return " ".join(random.sample(self.get_data(), k=number_of_words))