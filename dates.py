from datetime import datetime, timedelta

def calculate_weeks(year):
    # 1월 1일이 속한 주의 월요일로 시작
    start_date = datetime(year, 1, 1)
    if start_date.weekday() != 0:  # 월요일이 아니면 그 전으로 이동
        start_date -= timedelta(days=start_date.weekday())
    
    # 시작 날짜가 이전 연도에 속한 경우, 다음 주 월요일로 이동
    if start_date.year < year:
        start_date += timedelta(days=7)

    today = datetime.today()
    end_date = min(datetime(year, 12, 31), today)

    weeks = []
    
    while start_date <= end_date:
        week_start = start_date
        week_end = start_date + timedelta(days=6)

        # 현재 주차(오늘이 속한 주)는 포함하지 않음
        if week_start <= today <= week_end:
            break

        # 목요일 기준으로 소속 연/월 결정
        ref_date = week_start + timedelta(days=3)
        week_year = ref_date.year
        week_month = ref_date.month

        # >>> 연도 경계 처리: 다음 해로 넘어가는 주는 제외 <<<
        if week_start.year > year:
            break

        # 월의 첫날
        first_day_of_month = datetime(week_year, week_month, 1)
        first_day_week_start = first_day_of_month - timedelta(days=first_day_of_month.weekday())
        first_day_week_end = first_day_week_start + timedelta(days=6)

        if first_day_week_start <= first_day_of_month + timedelta(days=(3 - first_day_of_month.weekday()) % 7) <= first_day_week_end:
            month_week1_start = first_day_week_start
        else:
            month_week1_start = first_day_week_start + timedelta(days=7)

        week_number_in_month = ((week_start - month_week1_start).days // 7) + 1

        week_start_day = week_start.strftime('%Y%m%d')
        week_end_day = week_end.strftime('%Y%m%d')
        weeks.append((week_year, week_month, week_number_in_month, week_start_day, week_end_day))
        
        start_date += timedelta(days=7)

    return weeks


if __name__ == "__main__":
    # for debugging
    year = 2022
    weeks = calculate_weeks(year)
    
    for week_year, week_month, week_number_in_month, week_start_day, week_end_day in weeks:
        print(f"{week_year}Y {week_month}M {week_number_in_month}TH: {week_start_day} ~ {week_end_day}")
