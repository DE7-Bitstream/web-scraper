import requests
from bs4 import BeautifulSoup
import csv
from dates import calculate_weeks
from __init__ import *


def get_bs_from_days(start_day, end_day) -> BeautifulSoup:
    HEADER = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36" }
    url = f"https://www.melon.com/chart/week/index.htm?classCd=GN0000&moved=Y&startDay={start_day}&endDay={end_day}"
    
    response = requests.get(url, headers=HEADER)
    bs = BeautifulSoup(response.text, "html.parser")
    
    return bs

def parse_chart(bs) -> list:
    '''
    bs를 기반으로 차트 정보를 파싱하여 리스트로 반환
    '''
    songs = []
    for tr in bs.select("tr"):
        rank = tr.select_one(".rank")
        title = tr.select_one(".wrap_song_info .rank01 a")
        performer = tr.select_one(".wrap_song_info .rank02 a")
        
        if rank and title and performer:
            songs.append({
                "rank": rank.get_text(strip=True),
                "title": title.get_text(strip=True),
                "performer": performer.get_text(strip=True)
            })
    
    return songs

def crawl_data_by_days_url(start_day, end_day) -> list:
    bs = get_bs_from_days(start_day, end_day)
    chart = parse_chart(bs)
    return chart

def crawl_and_write_data_by_year(year) -> None:
    weeks = calculate_weeks(year)
    output_file = f"{CSV_DIR}/melon_chart_weekly_{year}.csv"

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["year", "month", "week_number_in_month", "rank", "song_name", "song_performer"])

        for week_year, week_month, week_number_in_month, week_start_day, week_end_day in weeks:
            chart = crawl_data_by_days_url(week_start_day, week_end_day)

            for item in chart:
                writer.writerow([
                    week_year,
                    week_month,
                    week_number_in_month,
                    item["rank"],
                    item["title"],
                    item["performer"]
                ])

if __name__ == "__main__":
    years = YEARS

    for year in years:
        crawl_and_write_data_by_year(year)