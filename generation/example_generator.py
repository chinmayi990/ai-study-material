import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ExampleGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    def generate_examples(self, topic, level="Beginner"):
        """Generate real-world examples using Groq API."""
        try:
            # Define prompt based on difficulty level
            prompts = {
                "Beginner": f"Generate 3 simple, relatable real-world examples of {topic} that a beginner can easily understand. Focus on everyday applications and simple scenarios that connect to common experiences.",
                "Intermediate": f"Generate 3 industry-relevant real-world examples of {topic} that demonstrate professional applications and technical implementations. Show how {topic} is used in business and technology contexts.",
                "Advanced": f"Generate 3 cutting-edge, advanced real-world examples of {topic} that highlight research applications, innovative implementations, and frontier technologies. Focus on advanced use cases and emerging trends."
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
            # Fallback to original examples if API fails
            print(f"Error generating examples with Groq: {e}")
            return self._fallback_examples(topic, level)
    
    def _fallback_examples(self, topic, level):
        """Fallback examples when model is unavailable"""
        
        examples = {
            "Beginner": f"""Real-World Examples of {topic}:

1. Everyday Application: {topic} can be seen in daily activities like organizing your workspace or planning your schedule. Just as you categorize tasks by priority, {topic} helps structure information systematically.

2. Simple Scenario: Think about following a recipe while cooking. The step-by-step process mirrors how {topic} works - each step builds on the previous one to achieve the desired outcome.

3. Relatable Context: When using a smartphone app, the intuitive interface you interact with is designed using principles of {topic}, making complex technology accessible and user-friendly.""",
            
            "Intermediate": f"""Real-World Examples of {topic}:

1. Industry Application: E-commerce platforms use {topic} to personalize user experiences, analyze purchasing patterns, and optimize product recommendations, leading to increased customer satisfaction and sales.

2. Professional Context: Project management teams apply {topic} principles to coordinate multiple tasks, allocate resources efficiently, and track progress across complex initiatives with many stakeholders.

3. Technical Implementation: Modern software systems leverage {topic} to handle data processing, ensure system reliability, and maintain performance even under high user load conditions.""",
            
            "Advanced": f"""Real-World Examples of {topic}:

1. Cutting-Edge Research: Leading technology companies are applying {topic} in developing autonomous systems that can make complex decisions in real-time, processing vast amounts of sensor data with minimal latency.

2. Advanced Application: In financial markets, {topic} powers algorithmic trading systems that analyze market conditions, predict trends, and execute transactions at microsecond intervals.

3. Innovation Frontier: Research institutions use {topic} in breakthrough applications like drug discovery, climate modeling, and artificial intelligence, pushing the boundaries of what's computationally possible."""
        }