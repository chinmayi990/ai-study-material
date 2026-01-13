
import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class QuizGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    def generate_quiz(self, topic, level):
        """Generate quiz questions based on topic and difficulty using Groq API"""
        try:
            # Define prompt based on difficulty level
            prompts = {
                "Beginner": f"Generate 3 multiple choice quiz questions about {topic} for beginners. Each question should have 4 options (A, B, C, D) with one correct answer. Include the correct answer and a brief explanation. Format as JSON with fields: question, options (array), correct (index 0-3), explanation.",
                "Intermediate": f"Generate 3 multiple choice quiz questions about {topic} for intermediate learners. Each question should have 4 options (A, B, C, D) with one correct answer. Include the correct answer and a brief explanation. Format as JSON with fields: question, options (array), correct (index 0-3), explanation.",
                "Advanced": f"Generate 3 multiple choice quiz questions about {topic} for advanced learners. Each question should have 4 options (A, B, C, D) with one correct answer. Include the correct answer and a detailed explanation. Format as JSON with fields: question, options (array), correct (index 0-3), explanation."
            }
            
            prompt = prompts.get(level, prompts["Beginner"])
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-8b-instant",  # Using Llama 3.1 model
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # Extract JSON from the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                try:
                    quiz_data = json.loads(json_str)
                    return quiz_data
                except json.JSONDecodeError:
                    # If JSON parsing fails, return fallback quiz
                    print("Failed to parse JSON from Groq response")
                    return self._fallback_quiz(topic, level)
            else:
                # If no JSON found, return fallback quiz
                print("No JSON found in Groq response")
                return self._fallback_quiz(topic, level)
        except Exception as e:
            # Fallback to original quiz if API fails
            print(f"Error generating quiz with Groq: {e}")
            return self._fallback_quiz(topic, level)
    
    def _fallback_quiz(self, topic, level):
        """Fallback quiz when model is unavailable"""
        quizzes = {
            "Beginner": self._beginner_quiz(topic),
            "Intermediate": self._intermediate_quiz(topic),
            "Advanced": self._advanced_quiz(topic)
        }
        
        return quizzes.get(level, quizzes["Beginner"])
    
    def _beginner_quiz(self, topic):
        return [
            {
                "question": f"What is the primary purpose of {topic}?",
                "options": [
                    f"To provide a foundation for understanding the subject",
                    f"To complicate simple concepts",
                    f"To replace practical experience",
                    f"None of the above"
                ],
                "correct": 0,
                "explanation": f"{topic} serves as a foundational concept that helps learners build understanding."
            },
            {
                "question": f"Which best describes {topic} at a beginner level?",
                "options": [
                    f"A complex theoretical framework",
                    f"A basic concept with practical applications",
                    f"An advanced research topic",
                    f"A specialized professional tool"
                ],
                "correct": 1,
                "explanation": f"For beginners, {topic} is best understood as a basic concept with clear practical uses."
            },
            {
                "question": f"What should be your first step when learning {topic}?",
                "options": [
                    f"Master advanced techniques immediately",
                    f"Understand basic definitions and simple examples",
                    f"Skip fundamentals and focus on applications",
                    f"Memorize without understanding"
                ],
                "correct": 1,
                "explanation": "Starting with basics and simple examples provides the best foundation for learning."
            }
        ]
    
    def _intermediate_quiz(self, topic):
        return [
            {
                "question": f"How does {topic} integrate with other concepts?",
                "options": [
                    f"Through interconnected principles and shared applications",
                    f"It operates in complete isolation",
                    f"Only through manual intervention",
                    f"It doesn't integrate with anything"
                ],
                "correct": 0,
                "explanation": f"{topic} typically connects with related concepts through shared principles."
            },
            {
                "question": f"What distinguishes intermediate understanding of {topic}?",
                "options": [
                    f"Ability to apply concepts to complex scenarios",
                    f"Simple memorization only",
                    f"Avoiding practical applications",
                    f"Ignoring theoretical foundations"
                ],
                "correct": 0,
                "explanation": "Intermediate learners can analyze and apply concepts to varied situations."
            },
            {
                "question": f"In practical applications, {topic} is most effective when:",
                "options": [
                    f"Customized to specific contexts and requirements",
                    f"Applied without any modifications",
                    f"Used in isolation from other methods",
                    f"Theory is completely ignored"
                ],
                "correct": 0,
                "explanation": "Effective application requires adapting principles to specific contexts."
            }
        ]
    
    def _advanced_quiz(self, topic):
        return [
            {
                "question": f"What are current research challenges in {topic}?",
                "options": [
                    f"Scalability, complexity, and integration with emerging technologies",
                    f"There are no challenges remaining",
                    f"Only basic implementation issues",
                    f"Lack of any theoretical foundation"
                ],
                "correct": 0,
                "explanation": f"Advanced work in {topic} faces ongoing challenges in scaling and integration."
            },
            {
                "question": f"How might {topic} evolve with new technologies?",
                "options": [
                    f"Through integration with AI, novel algorithms, and interdisciplinary approaches",
                    f"It will remain completely static",
                    f"By reverting to older methods",
                    f"Evolution is impossible"
                ],
                "correct": 0,
                "explanation": f"{topic} continues to evolve as new technologies and methods emerge."
            },
            {
                "question": f"What critical analysis is needed for {topic}?",
                "options": [
                    f"Evaluation of assumptions, limitations, and alternative approaches",
                    f"No analysis is necessary",
                    f"Only historical context matters",
                    f"Critical thinking is irrelevant"
                ],
                "correct": 0,
                "explanation": "Advanced understanding requires critical evaluation of methods and assumptions."
            }
        ]
