from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
import logging
# Add the SerperDevTool for general search capabilites
search_tool = SerperDevTool()

# Define agents
recommendation_agent = Agent(
    role="Travel Recommendation Specialist",
    goal="Provide personalized travel recommendations to users for their desired {destination}",
    backstory="You are a travel expert skilled at finding and suggesting the best options for travelers.",
    verbose=False
)

search_agent = Agent(
    role="Search Specialist",
    goal="Find travel deals for flights, hotels, and tours, for the specified {destination}",
    backstory="You are adept at scouring the web and APIs for the most accurate and up-to-date travel information.",
    tools=[search_tool],
    verbose=False
)

chat_agent = Agent(
    role="Interactive Travel Assistant",
    goal="Respond to user queries and guide them through the booking process.",
    backstory="You are a friendly and knowledgeable assistant who loves helping people plan their perfect trip.",
    verbose=False
)

# Define tasks
fetch_travel_deals = Task(
    description="Search for travel deals including flights, hotels, and tours, for the specifed {destination}",
    expected_output="A list of travel deals tailored to the destinaton structured JSON object containing the top 5 deals for flights, hotels, and tours.",
    agent=search_agent,
    verbose=False
)

generate_recommendations = Task(
    description="Analyze user preferences and travel deals to generate tailored travel package recommendations for the travelers {destination}.",
    expected_output="A list of three personalized travel packages with pricing and key details.",
    agent=recommendation_agent,
    verbose=False
)

handle_queries = Task(
    description="Interpret and respond to user queries about travel, such as pricing, availability, and recommendations for the {destination}",
    expected_output="Clear and concise responses to user inquiries, addressing their specific questions.",
    agent=chat_agent,
    verbose=False
)



# Create the crew
crew = Crew(
    agents=[recommendation_agent, search_agent, chat_agent],
    tasks=[fetch_travel_deals, generate_recommendations, handle_queries],
    process=Process.sequential,
    verbose=False
)

logger=logging()

def get_travel_recommendations(destination, interests, budget, start_date, end_date):
    """
    Triggers CrewAI agents to fetch travel deals and generate recommendations.
    """
    inputs = {
        "destination": destination,
        "interests": interests,
        "budget": budget,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    try:
        results = crew.kickoff(inputs=inputs)
        
        # Assuming results contain recommendations in the desired format
        if isinstance(results, list) and all('title' in r and 'price' in r and 'details' in r and 'image' in r for r in results):
            return {"recommendations": results}
        else:
            # Log unexpected structure for debugging
            logger.error(f"Unexpected result structure: {results}")
            return {"error": "Received unexpected data format from CrewAI"}
    except Exception as e:
        logger.error(f"Error fetching travel recommendations: {str(e)}", exc_info=True)
        return {"error": str(e)}

# def get_travel_recommendations(destination, interests, budget, start_date, end_date):
#     """
#     Triggers CrewAI agents to fetch travel deals and generate recommendations.
#     """
#     inputs = {
#         "destination": destination,
#         "interests": interests,
#         "budget": budget,
#         "start_date": start_date.isoformat(),
#         "end_date": end_date.isoformat(),
#     }
#     try:
#         results = crew.kickoff(inputs=inputs)
#         print(results)
#         return results
#     except Exception as e:
#         return {"error": str(e)}

