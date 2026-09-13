import re


def parse_budget(value: str) -> int:
    text = str(value or "").lower().replace(" ", "")
    matches = re.findall(r"\d+(?:[.,]\d+)?", text)
    if not matches:
        return 0
    number = float(matches[0].replace(",", "."))
    if "кк" in text or (number < 20 and "к" in text):
        return int(number * 1_000_000)
    if "к" in text or "тыс" in text or number < 20_000:
        return int(number * 1000) if number < 20_000 else int(number)
    return int(number)


def score_application(row: dict) -> dict:
    score = 0
    reasons = []

    deadline = (row.get("deadline") or "").lower()
    if any(token in deadline for token in ("не сроч", "подумаем", "следующ", "когда получится")):
        pass
    elif any(token in deadline for token in ("сегодня", "завтра", "срочно", "2 дн", "два дн", "48 час")):
        score += 30
        reasons.append("короткий срок")
    elif "недел" in deadline:
        score += 20
        reasons.append("срок в пределах недели")
    elif "месяц" in deadline:
        score += 4 if ("два" in deadline or "2" in deadline) else 10

    budget = parse_budget(row.get("budget") or "")
    if budget >= 400_000:
        score += 28
        reasons.append("высокий бюджет")
    elif budget >= 150_000:
        score += 16
        reasons.append("уверенный бюджет")
    elif budget >= 80_000:
        score += 8

    size = row.get("company_size") or ""
    if "200" in size:
        score += 18
        reasons.append("крупная компания")
    elif "51" in size:
        score += 12
        reasons.append("средний парк")
    elif "11" in size:
        score += 6

    if (row.get("role") or "").lower() == "руководитель":
        score += 12
        reasons.append("решение принимает руководитель")

    niche = (row.get("business_niche") or "").lower()
    if any(token in niche for token in ("дилер", "автопарк", "парк", "коллекц")):
        score += 10
        reasons.append("плотный бизнес-контекст")

    volume = f"{row.get('task_volume') or ''} {row.get('need_volume') or ''}".lower()
    if any(token in volume for token in ("полный", "парк", "несколько", "регуляр")):
        score += 8
        reasons.append("объём выше разового")

    if score >= 68:
        temperature = "hot"
        label = "Горячий"
        need_manager = True
    elif score >= 26:
        temperature = "warm"
        label = "Тёплый"
        need_manager = score >= 40
    else:
        temperature = "cold"
        label = "Холодный"
        need_manager = False

    product = (row.get("product") or "").lower()
    if any(token in product for token in ("керам", "плён", "плен")):
        department = "Защита кузова"
    elif any(token in product for token in ("хим", "салон", "музык")):
        department = "Кабинный сервис"
    elif any(token in product for token in ("полир", "детейл")):
        department = "Детейлинг"
    else:
        department = "Клиентский контур"

    payload = dict(row)
    payload.update(
        {
            "score": score,
            "temperature": temperature,
            "temperature_label": label,
            "need_manager": need_manager,
            "department": department,
            "analysis": ", ".join(reasons) or "нейтральный профиль",
        }
    )
    return payload
