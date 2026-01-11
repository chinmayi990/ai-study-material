from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

class ContentGenerator:
    def __init__(self):
        try:
            self.generator = pipeline("text-generation", model="gpt2")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.generator = None
    
    def generate_content(self, topic, level):
        """Generate educational content based on topic and difficulty level"""
        
        prompts = {
            "Beginner": f"""Explain {topic} in simple terms for beginners:
            
Definition: What is {topic}?
Basic Concepts: Key ideas to understand
Why It Matters: Practical importance
Getting Started: First steps to learn

Focus on clear, simple language suitable for someone new to this subject.""",
            
            "Intermediate": f"""Explain {topic} for intermediate learners:
            
Core Principles: Deeper understanding of {topic}
Key Mechanisms: How it works in detail
Applications: Real-world uses and implementations
Common Patterns: Frequently encountered scenarios

Assume basic knowledge and provide more technical depth.""",
            
            "Advanced": f"""Provide an advanced explanation of {topic}:
            
Theoretical Foundations: Academic and research perspectives
Complex Applications: Cutting-edge implementations
Critical Analysis: Strengths, limitations, and debates
Future Directions: Emerging trends and innovations

Use technical language appropriate for experts in the field."""
        }
        
        prompt = prompts.get(level, prompts["Beginner"])
        
        if self.generator:
            try:
                result = self.generator(
                    prompt,
                    max_length=400,
                    num_return_sequences=1,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True
                )
                return result[0]['generated_text']
            except Exception as e:
                print(f"Generation error: {e}")
                return self._fallback_content(topic, level)
        else:
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