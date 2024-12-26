from src.wandersmart.crew import get_travel_recommendations
import datetime

if __name__ == "__main__":
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 1, 10)
    response = get_travel_recommendations(
        destination="Europe",
        interests=["History", "Art"],
        budget=2000,
        start_date=start_date,
        end_date=end_date
    )
    print(response)
