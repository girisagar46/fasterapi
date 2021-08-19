import fastapi

from models.location import Location
from models.umbrella_status import UmbrellaStatus
from service.live_weather_service import get_live_weather_report

router = fastapi.APIRouter()


@router.get('/weather_api/umbrella', response_model=UmbrellaStatus)
async def do_i_need_an_umbrella(location: Location = fastapi.Depends()):
	data = await get_live_weather_report(location)
	weather = data.get("weather", {})
	category = weather.get("category", "UNKNOWN")
	forecast = data.get("forecast", {})
	temp = forecast.get("temp", 0.0)
	bring = category.lower().strip() == "rain"
	umbrella = UmbrellaStatus(bring_umbrella=bring, temp=temp, weather=category)
	return umbrella
