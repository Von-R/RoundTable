import json
import random
import openai
import logging

# Your OpenAI API keys for each agent
api_keys = {}
file = open("agent_keys.txt", "r")
api_keys_lines = file.read().splitlines()

for line in api_keys_lines:
    parts = [x.strip() for x in line.split("=")]
    key = parts[0]
    value = parts[1] if len(parts) > 1 else None
    if value:
        api_keys[key] = value
    logging.info("Number of keys: " + str(len(api_keys)))

# Load personality data and initial topic data from JSON files
with open("personalities.json") as personality_file:
    personalities = json.load(personality_file)["personalities"]

with open("topics.json") as topics_file:
    initial_topics = json.load(topics_file)["initial_topics"]

# Initialize agents with random personalities and velocities
agents = []
for _ in range(len(personalities)):
    # Agent is given personality
    random_personality = random.choice(list(personalities.keys()))
    agent = personalities.pop(random_personality)

    # Talkativeness range is stored in var
    talkativeness_range = personalities[agent]["talkativeness"]
    # Var used to gen randon talkativeness within range
    agent_talkativeness = random.uniform(talkativeness_range[0], talkativeness_range[1])

    # Assign API key to agent

    # Fully initialized agent is appended to list
    agents.append({"personality": agent, "talkativeness": agent_talkativeness})

for agent, api_key in zip(agents, api_keys.values()):
    agent['api_key'] = api_key

# Select a random initial topic
current_topic = random.choice(initial_topics)

# Create the API prompts for each agent
# Initialize empty list
api_prompts = []

# Loop through each agent: initialize the prompt and set the API key
for i, api_key in enumerate(api_keys):
    personality = personalities[agents[i]["personality"]]
    initial_topic = random.choice(initial_topics)

    prompt = f"You are a character engaging in a lively discussion with others. You will reply to them in-character and\
    on topic. This is your character: "
    prompt += f"Personality: {personality['name']}\n"
    prompt += f"Language Style: {personality['language_style']}\n"
    prompt += f"Character topics of Interest: {', '.join(personality['topics_of_interest'])}\n"
    prompt += f"Initial Topic: {initial_topic}\n"

    # Set the API key for the current agent
    agent['api_key'] = api_key

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

    while True:
        restart = True
        for agent in agents:
            agent_key = f"agent_{agent}_api_key"
            # Determine whether the agent responds in this turn based on talkativeness or if it's the first turn
            if random.random() <= agent["talkativeness"]:
                # Ensure the agent doesn't respond to their own message
                if conversation_history == [] or conversation_history[-1]["sender"] != agent["personality"]:
                    response = "Placeholder response"  # Replace with actual response generation

                    if api_keys.get(agent_key):
                        response = openai.Completion.create(
                            model="davinci",
                            prompt=api_prompts[agents.index(agent)],
                            temperature=0.9,
                            api_key=api_keys[agent_key]
                        )
                    restart = False
                    # Append the agent's response to the conversation history
                    conversation_history.append({"sender": agent["personality"], "content": response})
                    if restart == False:
                        break

        if restart == False:
            break

    current_turn += 1

# Print the conversation history
for message in conversation_history:
    print(f"{message['sender']}: {message['content']}")
