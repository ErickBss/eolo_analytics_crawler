from playwright.async_api import async_playwright
from models.weather import Weather


async def crawler(final_response: list[Weather]):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        result = {
            "hour": "",
            "temperature": "",
            "wind_speed": "",
            "wind_direction": "",
            "real_feal": "",
            "humidity": "",
        }

        await page.goto(
            "https://www.accuweather.com/en/br/s%C3%A3o-paulo/45881/hourly-weather-forecast/45881",
            wait_until="domcontentloaded",
        )
        print("passed")
        await page.wait_for_selector(".hourly-wrapper, content-module")
        print("page loaded")
        weather_details = await (
            await page.query_selector(".hourly-wrapper, content-module")
        ).query_selector_all(".accordion-item, hour")

        for detail_element in weather_details:
            weather = Weather()
            weather.set_attr("source_id", 2)
            result["hour"] = await detail_element.query_selector(".date")
            result["temperature"] = await detail_element.query_selector(".temp, metric")
            result["real_feal"] = await detail_element.query_selector(
                ".real-feel__text"
            )

            for key in result.keys():
                if type(result[key]) is not str:
                    if key == "hour":
                        value = await result[key].inner_text()
                        weather.set_hour(value)
                    elif key == "humidity":
                        value = await result[key].inner_text()
                        weather.set_humidity(value)
                    else:
                        value = await result[key].inner_text()
                        weather.set_attr(key, value)

            extra_details_elements = await (
                await detail_element.query_selector(".panel, no-realfeel-phrase")
            ).query_selector_all("p")

            for extra_detail in extra_details_elements:
                content = await extra_detail.inner_text()
                category = content.splitlines()[0]

                if category == "Wind":
                    wind_details = await (
                        await extra_detail.query_selector(".value")
                    ).inner_text()
                    wind_details = wind_details.split()

                    weather.set_attr("wind_direction", wind_details[0])
                    weather.set_attr("wind_speed", wind_details[1])
                elif category == "Humidity":
                    value = await (
                        await extra_detail.query_selector(".value")
                    ).inner_text()
                    weather.set_humidity(value)

            final_response.append(weather)
            result = result.fromkeys(result, "")

        await browser.close()
