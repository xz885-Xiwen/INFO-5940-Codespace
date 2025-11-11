# Assignment 2: Multi-Agent Travel Planner - Reflection

## What I Learned from Multi-Agent Workflow Implementation

Implementing this multi-agent system revealed the power of task decomposition in AI applications. The separation between the Planner and Reviewer agents created a natural pipeline that mirrors real-world workflows: generation followed by validation. This architecture demonstrates how specialized agents with distinct capabilities can collaborate to produce higher-quality outputs than a single monolithic agent.

The most valuable insight was understanding the complementary nature of knowledge-based generation versus tool-augmented verification. The Planner operates purely from its training data to create comprehensive itineraries, while the Reviewer uses real-time internet searches to ground-truth specific claims. This division prevents the planning phase from being slowed by excessive tool calls while ensuring the final output is factually validated.

## Challenges and Solutions

The primary challenge was crafting system prompts that would produce consistent, structured outputs. Initially, I struggled with ensuring the Reviewer would output both a Delta List and a complete revised itinerary. The solution was to explicitly structure the prompt with markdown headers (## Delta List, ## Revised Itinerary) and provide clear instructions for each section.

Another challenge was balancing prompt specificity with flexibility. Travel planning varies significantly by destination, budget, and interests. I addressed this by instructing the Planner to always include certain elements (times, costs, logistics) while remaining adaptable to different travel scenarios.

Testing the async workflow integration required understanding how the Runner.run() method interfaces with agent definitions, particularly how tools are passed through the tools parameter to enable the Reviewer's internet search capability.

## Creative Design Choices

I designed the Reviewer's instructions to be proactive in its fact-checking approach, providing example search queries (e.g., "opening hours [venue] [city]") to encourage thorough validation. This teaches the agent how to decompose validation tasks into specific, searchable questions.

For the Planner, I emphasized geographic clustering and pacing considerations to produce itineraries that feel realistic rather than exhausting bullet-point lists. The instruction to avoid over-scheduling encourages human-centered planning.

## External Tools and GenAI Assistance

I used the provided template's architecture as the foundation, focusing my effort on the system prompts themselves. The assignment template provided excellent scaffolding with the tool logging system and orchestration helpers, allowing me to concentrate on agent behavior design rather than infrastructure.
