from playwright.async_api import async_playwright
from models.weather import Weather


async def crawler(final_response: list[Weather]):
    async with async_playwright() as p:
        # inicializa navegador
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

        # abre página da fonte
        await page.goto(
            "https://weather.com/pt-BR/clima/horaria/l/dfb390d5d0537ed3c80f13693bce4fb5ab75fb5fa1ddd5c46fb61fc04264005d",
            wait_until="networkidle",
        )
        print("page loaded")

        await page.wait_for_selector("#sp_message_iframe_1165283")
        privacy_button = page.frame_locator("#sp_message_iframe_1165283").get_by_title(
            "Aceitar todos"
        )
        await privacy_button.click()

        hourly_container = await page.query_selector(
            ".HourlyForecast--DisclosureList--MQWP6"
        )
        items = await hourly_container.query_selector_all("details")

        # busca informações no html e armezena na classe
        for item in items:
            weather = Weather()
            weather.set_attr("source_id", 1)
            result["hour"] = await item.query_selector("[data-testid='daypartName']")
            selected_hour = await result["hour"].inner_text()

            if len(selected_hour) > 0 and selected_hour == "0:00":
                break

            result["temperature"] = await item.query_selector(
                "[data-testid='TemperatureValue']"
            )
            wind_element = await item.query_selector("[data-testid='wind']")
            wind_details = await wind_element.inner_text()
            wind_details = wind_details.split()

            weather.set_attr("wind_direction", wind_details[0])
            weather.set_attr("wind_speed", wind_details[1])

            result["real_feal"] = await item.query_selector(
                "li[data-testid='FeelsLikeSection'], [data-testid='TemperatureValue']"
            )
            result["humidity"] = await item.query_selector(
                "li[data-testid='HumiditySection']"
            )

            for key in result.keys():
                if type(result[key]) is not str:
                    if key == "humidity":
                        value = await result[key].inner_text()
                        humidity_array = value.splitlines()

                        if len(humidity_array) == 2:
                            weather.set_humidity(humidity_array[1])
                    elif key == "hour":
                        value = await result[key].inner_text()
                        weather.set_hour(value)
                    else:
                        value = await result[key].inner_text()
                        weather.set_attr(key, value)

            final_response.append(weather)
            result = result.fromkeys(result, "")

        await browser.close()
