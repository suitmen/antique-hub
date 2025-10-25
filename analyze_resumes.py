import os
import re

def analyze_resumes():
    # Dictionary to store cities and their specializations
    cities_data = {}
    # Dictionary to store specializations with ages
    specializations_data = {}
    
    # Go through all resume files
    for i in range(1, 101):
        filename = f"resumes/resume_{i}.txt"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Extract city
                city_match = re.search(r"Город проживания: (.+)", content)
                city = city_match.group(1) if city_match else "Не указан"
                
                # Extract specialization
                spec_match = re.search(r"Профессия: (.+)", content)
                specialization = spec_match.group(1) if spec_match else "Не указана"
                
                # Extract age
                age_match = re.search(r"Возраст: (\d+)", content)
                age = int(age_match.group(1)) if age_match else 0
                
                # Add to cities dictionary
                if city not in cities_data:
                    cities_data[city] = set()
                cities_data[city].add(specialization)
                
                # Add to specializations dictionary
                if specialization not in specializations_data:
                    specializations_data[specialization] = []
                specializations_data[specialization].append(age)
    
    # Generate markdown output
    markdown_output = "# Анализ резюме по городам и специальностям\n\n"
    
    # Sort cities alphabetically
    sorted_cities = sorted(cities_data.keys())
    
    for city in sorted_cities:
        markdown_output += f"## {city}\n\n"
        specializations = sorted(cities_data[city])
        for spec in specializations:
            markdown_output += f"- {spec}\n"
        markdown_output += "\n"
    
    # Create specialization analysis with average ages
    markdown_output += "# Средний возраст по специальностям\n\n"
    markdown_output += "| Специальность | Средний возраст | Количество специалистов |\n"
    markdown_output += "|---------------|-----------------|-------------------------|\n"
    
    # Sort specializations alphabetically
    sorted_specializations = sorted(specializations_data.keys())
    
    for spec in sorted_specializations:
        ages = specializations_data[spec]
        avg_age = sum(ages) / len(ages) if ages else 0
        markdown_output += f"| {spec} | {avg_age:.1f} лет | {len(ages)} |\n"
    
    # Also create a summary section
    markdown_output += "\n# Сводная таблица по городам\n\n"
    markdown_output += "| Город | Количество специалистов | Специальности |\n"
    markdown_output += "|-------|------------------------|---------------|\n"
    
    for city in sorted_cities:
        specializations = sorted(cities_data[city])
        spec_list = ", ".join(specializations)
        markdown_output += f"| {city} | {len(specializations)} | {spec_list} |\n"
    
    return markdown_output

# Run the analysis and save to file
if __name__ == "__main__":
    result = analyze_resumes()
    with open("resume_analysis.md", "w", encoding="utf-8") as f:
        f.write(result)
    print("Анализ завершен. Результаты сохранены в resume_analysis.md")
    print(result[:1000] + "..." if len(result) > 1000 else result)  # Print first 1000 chars