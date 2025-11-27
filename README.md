# Example Usage & Testing

This document provides example queries and expected behaviors for testing the Isha Programs MCP server.

## Tool: search_programs_by_location

### Basic Country Search
```
Query: "Show me yoga programs in India"
Tool Call: search_programs_by_location(country="India", limit=20)
Expected: List of programs in India with details
```

### City-Specific Search
```
Query: "What programs are available in Bangalore?"
Tool Call: search_programs_by_location(country="India", city="Bangalore", limit=20)
Expected: Programs specifically in Bangalore, India
```

### Multiple Countries
```
Query: "Show me programs in USA"
Tool Call: search_programs_by_location(country="USA", limit=20)
Expected: List of programs in United States
```

## Tool: search_programs_by_interest

### Specific Practice
```
Query: "I want to learn Surya Kriya"
Tool Call: search_programs_by_interest(interest="surya kriya")
Expected: All Surya Kriya programs globally
```

### Category Search
```
Query: "Show me meditation programs"
Tool Call: search_programs_by_interest(interest="meditation")
Expected: All meditation-related programs
```

### With Location Filter
```
Query: "Find Inner Engineering programs in USA"
Tool Call: search_programs_by_interest(interest="inner engineering", country="USA")
Expected: Inner Engineering programs in USA only
```

### Kriya Programs
```
Query: "What kriyas can I learn?"
Tool Call: search_programs_by_interest(interest="kriya")
Expected: All kriya-type programs (Shambhavi, Surya Kriya, etc.)
```

## Tool: search_programs_nearby

### Coordinate Search
```
Query: "Find programs near coordinates 12.9716, 77.5946"
Tool Call: search_programs_nearby(latitude=12.9716, longitude=77.5946)
Expected: Programs near Bangalore, India
```

### User Location
```
Query: "What programs are near me?" (with user sharing location)
Tool Call: search_programs_nearby(latitude=USER_LAT, longitude=USER_LON)
Expected: Programs sorted by distance from user
```

## Tool: get_program_details

### Specific Program
```
Query: "Tell me more about program ID 56924"
Tool Call: get_program_details(program_id="56924")
Expected: Detailed JSON information about that specific program
```

## Tool: filter_programs

### Online Programs
```
Query: "Show me online programs in India"
Tool Call: filter_programs(country="India", online=true, limit=20)
Expected: Only online programs in India
```

### Programs with Sadhguru
```
Query: "Find programs where Sadhguru will be present in USA"
Tool Call: filter_programs(country="USA", with_sadhguru=true)
Expected: Programs in USA featuring Sadhguru
```

### Language Filter
```
Query: "Show me Hindi language programs"
Tool Call: filter_programs(country="India", language="hindi")
Expected: Programs conducted in Hindi
```

### Combined Filters
```
Query: "Find online English programs with Sadhguru"
Tool Call: filter_programs(country="India", online=true, language="english", with_sadhguru=true)
Expected: Programs matching all criteria
```

## Tool: get_available_countries

### Discovery
```
Query: "Which countries have Isha programs?"
Tool Call: get_available_countries()
Expected: Complete list of countries with programs
```

## Tool: get_cities_in_country

### City Discovery
```
Query: "What cities in India have programs?"
Tool Call: get_cities_in_country(country="India")
Expected: List of Indian cities with programs
```

```
Query: "Which cities in USA offer Isha programs?"
Tool Call: get_cities_in_country(country="USA")
Expected: List of US cities with programs
```

## Tool: list_program_categories

### Category Discovery
```
Query: "What types of programs are available?"
Tool Call: list_program_categories()
Expected: Complete list of program categories with keywords
```

## Complex Multi-Step Queries

### Planning a Trip
```
User: "I want to attend a yoga retreat in India next month"
Steps:
1. list_program_categories() - Show retreat category
2. search_programs_by_interest(interest="retreat", country="India")
3. User selects a program
4. get_program_details(program_id=SELECTED_ID)
```

### Learning Path
```
User: "I'm new to Isha. What should I start with?"
Steps:
1. list_program_categories() - Show all categories
2. search_programs_by_interest(interest="inner engineering", country=USER_COUNTRY)
3. Explain Inner Engineering as the foundation program
```

### Local Discovery
```
User: "I live in Chennai. What can I do this weekend?"
Steps:
1. search_programs_by_location(country="India", city="Chennai", limit=10)
2. Filter results by upcoming weekend dates
3. Present options with registration links
```

## Expected Data Format

Each program result includes:

```
**Program Title**
- Category: Angamardana
- Date: 22 - 23 Nov 2025
- Time: 7:30AM - 6:15PM
- Location: Sadhguru Sannidhi, Bengaluru, India
- Fee: INR 3500
- Language: english
- Gender: unspecified
- Online: No
- With Sadhguru: No
- Program URL: https://isha.sadhguru.org/program-details/...
- Register: https://online.sadhguru.org/event-register?event=...
- Program ID: 78206
```

## Error Scenarios

### No Results Found
```
Query: "Programs in Antarctica"
Expected: Graceful message saying no programs found
```

### Invalid Program ID
```
Query: "Details for program 999999999"
Expected: Error message about invalid program ID
```

### API Rate Limiting
```
Expected: Appropriate error message if API rate limit hit
```

## Performance Notes

- Typical response time: 1-3 seconds
- Large result sets may take longer
- Coordinate searches may be slower due to distance calculations
- Consider setting reasonable limits (20-50 items)

## Integration Testing

Test with Claude Desktop by:

1. Asking conversational questions
2. Following up with refinements
3. Requesting multiple related searches
4. Combining information from multiple tools

Example conversation flow:
```
User: "I want to learn yoga"
→ list_program_categories()

User: "Tell me about the Yogasanas programs"
→ search_programs_by_interest(interest="yogasanas")

User: "Which of these are in Bangalore?"
→ filter previous results by location

User: "Tell me more about program #3"
→ get_program_details(program_id=...)

User: "How do I register?"
→ Provide registration URL from program details
```


