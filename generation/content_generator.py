
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    def generate_content(self, topic, level):
        """Generate structured, difficulty-specific explanation using Groq API."""
        try:
            # Define prompt based on difficulty level
            prompts = {
                "Beginner": f"Explain {topic} in simple terms suitable for beginners. Focus on the basic definition, purpose, and fundamental concepts. Make it easy to understand for someone with no prior knowledge. Include key aspects to learn and practical applications.",
                "Intermediate": f"Provide a detailed explanation of {topic} suitable for intermediate learners. Explain the underlying mechanisms, principles, and practical applications. Include how different components interact, various methodologies, and real-world use cases.",
                "Advanced": f"Deliver a comprehensive explanation of {topic} for advanced learners. Cover theoretical frameworks, complex implementations, current research, and critical analysis of different methodologies. Discuss innovations and future directions in the field."
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
            
            return chat_completion.choices[0].message.content
        except Exception as e:
            # Fallback to original content if API fails
            print(f"Error generating content with Groq: {e}")
            return self._fallback_content(topic, level)
    
    def _fallback_content(self, topic, level):
        """Fallback content when model is unavailable"""
        
        fallback = {
            "Beginner": f"""Understanding {topic} - Beginner Level

{topic} is a fundamental concept that serves as a building block for further learning. At the beginner level, focus on grasping the basic definition and understanding why this concept is important.

Key aspects to learn:
- The basic definition and purpose of {topic}
- Simple examples that demonstrate the concept
- How it relates to everyday situations
- The foundation it provides for more advanced learning

Start by familiarizing yourself with the terminology and basic principles. Don't worry about complex details initially - focus on building a solid foundational understanding.""",
            
            "Intermediate": f"""Understanding {topic} - Intermediate Level

{topic} represents an important concept that requires deeper analysis and practical application. At this level, you should understand not just what it is, but how and why it works.

Important considerations:
- The underlying mechanisms and principles
- How different components interact
- Various approaches and methodologies
- Application to real-world problems
- Common challenges and solutions

Build on your foundational knowledge by exploring more complex scenarios and understanding the nuances that exist in different contexts.""",
            
            "Advanced": f"""Understanding {topic} - Advanced Level

{topic} at an advanced level requires comprehensive understanding of theoretical frameworks, practical implementations, and critical analysis of current approaches.

Focus areas:
- Theoretical foundations and academic research
- Complex implementations and optimizations
- Critical evaluation of different methodologies
- Integration with other advanced concepts
- Contributing to innovation in the field

At this level, emphasis is on deep expertise, research capabilities, and the ability to push boundaries of current understanding."""
        }
        
        return fallback.get(level, fallback["Beginner"])
