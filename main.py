import json
import random
import openai

# Your OpenAI API keys for each agent
api_keys = ["YOUR_API_KEY_AGENT_1", "YOUR_API_KEY_AGENT_2", "YOUR_API_KEY_AGENT_3"]

# Load personality data and initial topic data from JSON files
with open("personality_data.json") as personality_file:
    personalities = json.load(personality_file)["personalities"]

with open("initial_topics.json") as topics_file:
    initial_topics = json.load(topics_file)["initial_topics"]

# Initialize agents with random personalities and velocities
agents = []
for _ in range(2):  # Assuming 2 agents for simplicity
    agent = random.choice(list(personalities.keys()))
    talkativeness_range = personalities[agent]["talkativeness"]
    agent_talkativeness = random.uniform(talkativeness_range[0], talkativeness_range[1])
    agents.append({"personality": agent, "talkativeness": agent_talkativeness})



# Select a random initial topic
current_topic = random.choice(initial_topics)

# Create the API prompts for each agent
# Initialize empty list
api_prompts = []

# Loop through each agent: initialize the prompt and set the API key
for i, api_key in enumerate(api_keys):
    personality = personalities[agents[i]["personality"]]
    initial_topic = random.choice(initial_topics)

    prompt = f"You are a character engaging in a lively discussion with others. This is your character: "
    prompt += f"Personality: {personality['name']}\n"
    prompt += f"Language Style: {personality['language_style']}\n"
    prompt += f"Character topics of Interest: {', '.join(personality['topics_of_interest'])}\n"
    prompt += f"Initial Topic: {initial_topic}\n"

    # Set the API key for the current agent
    openai.api_key = api_key

    # Create the API prompt for the current agent
    api_prompts.append(prompt)

# Initialize conversation history
conversation_history = []

# Simulate conversation for a certain number of turns
num_turns = 10  # Adjust the number of turns as needed
current_turn = 0

while current_turn < num_turns:
    # Shuffle the order of agents for a more natural conversation flow
    random.shuffle(agents)

    for agent in agents:
        # Determine whether the agent responds in this turn based on talkativeness
        if random.random() <= agent["talkativeness"]:
            response = "Placeholder response"  # Replace with actual response generation

            # Append the agent's response to the conversation history
            conversation_history.append({"sender": agent["personality"], "content": response})

    current_turn += 1

# Print the conversation history
for message in conversation_history:
    print(f"{message['sender']}: {message['content']}")
