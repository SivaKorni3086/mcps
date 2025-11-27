#!/usr/bin/env python3
"""
Isha Foundation Programs MCP Server using FastMCP

This MCP server provides tools to search and discover Isha Foundation programs
including yoga, meditation, kriyas, and other spiritual offerings.
"""

import random
import ssl
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

# API Configuration
ISHA_API_BASE = "https://www.ishafoundation.org/index.php"
SCHEDULE_API_BASE = "https://api.ishafoundation.org/scheduleApi/api.php"
USER_AGENT = "isha-programs-mcp/1.0-python"

# Program categories with their API category IDs
PROGRAM_CATEGORIES = [
    {
        "name": "Inner Engineering",
        "category_id": 5815,
        "keywords": ["inner engineering", "ie", "shambhavi", "shambhavi mahamudra"]
    },
    {
        "name": "Surya Shakti",
        "category_id": 148,
        "keywords": ["surya shakti"]
    },
    {
        "name": "Surya Kriya",
        "category_id": 122,
        "keywords": ["surya kriya"]
    },
    {
        "name": "Angamardana",
        "category_id": 124,
        "keywords": ["angamardana"]
    },
    {
        "name": "Bhuta Shuddhi",
        "category_id": 125,
        "keywords": ["bhuta shuddhi", "bhutashuddhi"]
    },
    {
        "name": "Yogasanas",
        "category_id": 121,
        "keywords": ["yogasanas", "yoga postures", "asanas", "hatha yoga"]
    },
    {
        "name": "Bhava Spandana",
        "category_id": 7,
        "keywords": ["bhava spandana", "bsp"]
    },
    {
        "name": "Shoonya Meditation",
        "category_id": 13,
        "keywords": ["shoonya", "shoonya meditation", "meditation"]
    },
    {
        "name": "Samyama",
        "category_id": 12,
        "keywords": ["samyama"]
    },
    {
        "name": "Guru Pooja",
        "category_id": 14,
        "keywords": ["guru pooja", "guru poornima"]
    },
    {
        "name": "21 Day Sadhana Program",
        "category_id": 259,
        "keywords": ["21 day sadhana", "21 days sadhana", "sadhana program"]
    },
    {
        "name": "Samyama Sadhana",
        "category_id": 105,
        "keywords": ["samyama sadhana"]
    },
    {
        "name": "Sunetra Eye Care",
        "category_id": 28,
        "keywords": ["sunetra", "eye care"]
    },
    {
        "name": "Yoga Chikitsa",
        "category_id": 207,
        "keywords": ["yoga chikitsa"]
    },
    {
        "name": "Ayur Sampoorna",
        "category_id": 17,
        "keywords": ["ayur sampoorna"]
    },
    {
        "name": "Joint and Musculoskeletal Disorders Program",
        "category_id": 132,
        "keywords": ["joint disorder", "musculoskeletal", "joint program"]
    },
    {
        "name": "Pancha Karma",
        "category_id": 208,
        "keywords": ["pancha karma", "panchkarma", "panchakarma"]
    },
    {
        "name": "Ayur Rasayana Intensive",
        "category_id": 16,
        "keywords": ["ayur rasayana intensive"]
    },
    {
        "name": "Ayur Sanjeevini",
        "category_id": 226,
        "keywords": ["ayur sanjeevini"]
    },
    {
        "name": "Yoga Marga",
        "category_id": 18,
        "keywords": ["yoga marga"]
    },
    {
        "name": "Ayur Rasayana",
        "category_id": 10,
        "keywords": ["ayur rasayana"]
    },
    {
        "name": "Diabetes Management Program",
        "category_id": 131,
        "keywords": ["diabetes", "diabetes management", "diabetes program"]
    },
    {
        "name": "Guru Poornima",
        "category_id": 22,
        "keywords": ["guru poornima"]
    }
]

def _get_category_id(interest: str) -> str:
    """
    Map an interest/keyword string to the corresponding API category ID.
    Returns empty string if no match found (will search all categories).
    """
    interest_lower = interest.lower().strip()
    
    for category in PROGRAM_CATEGORIES:
        # Check if interest matches category name
        if interest_lower == category["name"].lower():
            return str(category["category_id"])
        
        # Check if interest matches any keyword
        for keyword in category["keywords"]:
            if keyword in interest_lower or interest_lower in keyword:
                return str(category["category_id"])
    
    # No match found - return empty string to search all
    return ""


# Create FastMCP instance
mcp = FastMCP(
    name="Isha Programs MCP",
    instructions="""This MCP server provides comprehensive search and discovery for Isha Foundation programs worldwide.

USE THIS SERVER when users:
- Want to find yoga, meditation, or spiritual programs by location (country/city)
- Search for specific program types: Inner Engineering, Surya Shakti, Surya Kriya, Angamardana, Bhuta Shuddhi, Yogasanas, Bhava Spandana, Shoonya Meditation, Samyama, Guru Pooja, 21 Day Sadhana, Samyama Sadhana, Sunetra Eye Care, Yoga Chikitsa, Ayur Sampoorna, Joint Disorders Program, Pancha Karma, Ayur Rasayana, Diabetes Management, Yoga Marga, etc.
- Look for programs nearby using GPS coordinates
- Need details about program schedules, fees, languages, or registration
- Filter programs by criteria (online/offline, with Sadhguru, specific language)
- Ask about available countries or cities offering programs

DO NOT use this server for:
- Quotes or spiritual wisdom (use Quotes MCP instead)
- Calendar events or auspicious dates (use Calendar MCP instead)
- General spiritual questions not related to program registration

The server connects to Isha Foundation's official programs API and provides real-time information about upcoming programs globally."""
)

# Create HTTP client with SSL verification disabled
http_client = httpx.AsyncClient(
    headers={"User-Agent": USER_AGENT},
    verify=False,  # Disable SSL verification for this API
    timeout=30.0
)


def format_program(program: Dict[str, Any], index: Optional[int] = None) -> str:
    """Helper function to format programs for display"""
    prefix = f"{index}. " if index is not None else ""
    return f"""{prefix}**{program.get('title', 'N/A')}**
- Category: {program.get('program_category', 'N/A')}
- Date: {program.get('date', 'N/A')}
- Time: {program.get('time', 'N/A')}
- Location: {program.get('address', 'N/A')}, {program.get('country', 'N/A')}
- Fee: {program.get('currency', '')} {program.get('amount', 'N/A')}
- Language: {program.get('language', 'N/A')}
- Gender: {program.get('gender', 'N/A')}
- Online: {"Yes" if program.get('is_online') == "1" else "No"}
- With Sadhguru: {"Yes" if program.get('is_sadhguru') == "1" else "No"}
- Program URL: {program.get('program_url', 'N/A')}
- Register: {program.get('register_url', 'N/A')}
- Program ID: {program.get('program_id', 'N/A')}"""


def extract_programs(response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Helper function to extract programs from API response"""
    if not response_data or 'results' not in response_data:
        return []
    
    programs = []
    for result in response_data['results']:
        # Each result is a dict with a single key-value pair
        program = list(result.values())[0]
        programs.append(program)
    return programs


@mcp.tool()
async def search_programs_by_location(
    country: str,
    city: Optional[str] = None,
    limit: int = 20
) -> str:
    """
    Search for Isha Foundation programs by location (country and optional city).
    Returns upcoming programs in the specified location.
    
    Args:
        country: Country name (e.g., 'India', 'USA', 'UK')
        city: Optional city name to narrow down search
        limit: Maximum number of results to return (default: 20, max: 100)
    """
    try:
        params = {
            "option": "com_program",
            "Itemid": 250,
            "Submit": "Filter",
            "task": "filter",
            "program": 0,
            "cat": 0,
            "utm_medium": "yogalanding",
            "utm_content": "pgmspanel",
            "date": 0,
            "event": 0,
            "format": "json",
            "rejuvenation": 0,
            "utm_source": "mcp",
            "utm_campaign": "sgapp",
            "search": "fuzzy",
            "count": limit,
            "radius": "",
            "startrec": 0,
            "category": "",
            "latlong": "",
            "city": city or "",
            "country": country,
            "v": 2,
        }
        
        response = await http_client.get(SCHEDULE_API_BASE, params=params)
        response.raise_for_status()
        programs = extract_programs(response.json())
        
        if not programs:
            return f"No programs found in {city + ', ' if city else ''}{country}. Try a different location or check back later."
        
        formatted_programs = "\n---\n\n".join(
            format_program(program, idx + 1) for idx, program in enumerate(programs)
        )
        
        return f"Found {len(programs)} programs in {city + ', ' if city else ''}{country}:\n\n{formatted_programs}"
    
    except Exception as e:
        return f"Error searching programs: {str(e)}"


@mcp.tool()
async def search_programs_by_interest(
    interest: str,
    country: Optional[str] = "India",
    city: Optional[str] = None,
    limit: int = 20
) -> str:
    """
    Search for programs by category/interest. The interest is mapped to a specific program category ID.
    
    Supported program types:
    - Inner Engineering, Surya Shakti, Surya Kriya, Angamardana, Bhuta Shuddhi, Yogasanas
    - Bhava Spandana (BSP), Shoonya Meditation, Samyama, Guru Pooja, Guru Poornima
    - 21 Day Sadhana Program, Samyama Sadhana
    - Health programs: Sunetra Eye Care, Yoga Chikitsa, Ayur Sampoorna, Joint Disorders, Pancha Karma, Ayur Rasayana, Diabetes Management, Yoga Marga
    
    Args:
        interest: Type of program (e.g., 'Inner Engineering', 'Surya Kriya', 'Angamardana', 'Bhava Spandana', 'Shoonya', 'Samyama', 'Yogasanas', 'Bhuta Shuddhi', 'Pancha Karma', 'Diabetes')
        country: Country to filter results (default: "India"). Set to empty string "" to search globally.
        city: Optional city to filter results
        limit: Maximum number of results to return (default: 20, max: 100)
    """
    try:
        # Default country to India if not specified or None
        search_country = country if country is not None else "India"
        
        params = {
            "option": "com_program",
            "Itemid": 250,
            "Submit": "Filter",
            "task": "filter",
            "program": 0,
            "cat": 0,
            "utm_medium": "yogalanding",
            "utm_content": "pgmspanel",
            "date": 0,
            "event": 0,
            "format": "json",
            "rejuvenation": 0,
            "utm_source": "mcp",
            "utm_campaign": "sgapp",
            "search": "fuzzy",
            "count": limit,
            "radius": "",
            "startrec": 0,
            "category": _get_category_id(interest),
            "latlong": "",
            "city": city or "",
            "country": search_country,
            "v": 2,
        }
        
        response = await http_client.get(SCHEDULE_API_BASE, params=params)
        response.raise_for_status()
        programs = extract_programs(response.json())
        
        location_str = ""
        if city and search_country:
            location_str = f" in {city}, {search_country}"
        elif city:
            location_str = f" in {city}"
        elif search_country:
            location_str = f" in {search_country}"
        
        if not programs:
            return f"No programs found for \"{interest}\"{location_str}. Try a different category or location."
        
        formatted_programs = "\n---\n\n".join(
            format_program(program, idx + 1) for idx, program in enumerate(programs)
        )
        
        return f"Found {len(programs)} programs for \"{interest}\"{location_str}:\n\n{formatted_programs}"
    
    except Exception as e:
        return f"Error searching programs by interest: {str(e)}"


@mcp.tool()
async def search_programs_nearby(
    latitude: float,
    longitude: float,
    limit: int = 20
) -> str:
    """
    Search for programs near a specific location using latitude and longitude coordinates.
    Best for finding programs closest to the user's current location.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        limit: Maximum number of results to return (default: 20, max: 100)
    """
    try:
        params = {
            "option": "com_program",
            "Itemid": 250,
            "Submit": "Filter",
            "task": "filter",
            "program": 0,
            "cat": 0,
            "utm_medium": "yogalanding",
            "utm_content": "pgmspanel",
            "date": 0,
            "event": 0,
            "format": "json",
            "rejuvenation": 0,
            "utm_source": "mcp",
            "utm_campaign": "sgapp",
            "search": "fuzzy",
            "count": limit,
            "radius": "",
            "startrec": 0,
            "category": "",
            "latlong": f"{latitude},{longitude}",
            "city": "",
            "country": "",
            "v": 2,
        }
        
        response = await http_client.get(SCHEDULE_API_BASE, params=params)
        response.raise_for_status()
        programs = extract_programs(response.json())
        
        if not programs:
            return f"No programs found near coordinates ({latitude}, {longitude}). Try expanding your search area."
        
        formatted_programs = "\n---\n\n".join(
            format_program(program, idx + 1) for idx, program in enumerate(programs)
        )
        
        return f"Found {len(programs)} programs near ({latitude}, {longitude}):\n\n{formatted_programs}"
    
    except Exception as e:
        return f"Error searching programs nearby: {str(e)}"


@mcp.tool()
async def get_program_details(program_id: str) -> str:
    """
    Get detailed information about a specific program using its program ID.
    Use this to get more information about a program found through search.
    
    Args:
        program_id: The program ID (obtained from search results)
    """
    try:
        params = {
            "option": "com_program",
            "v": 2,
            "format": "json",
            "task": "details",
            "program_id": program_id,
        }
        
        response = await http_client.get(SCHEDULE_API_BASE, params=params)
        response.raise_for_status()
        details = response.json()
        
        import json
        return f"Program Details:\n\n{json.dumps(details, indent=2)}"
    
    except Exception as e:
        return f"Error fetching program details: {str(e)}"


@mcp.tool()
async def filter_programs(
    country: str = "India",
    online: Optional[bool] = None,
    with_sadhguru: Optional[bool] = None,
    language: Optional[str] = None,
    limit: int = 20
) -> str:
    """
    Filter a set of programs by specific criteria like online/offline, language, with Sadhguru, etc.
    This is useful for refining search results.
    
    Args:
        country: Country to search in (default: "India")
        online: Filter for online programs only (true) or in-person only (false)
        with_sadhguru: Filter for programs with Sadhguru's presence
        language: Filter by language (e.g., 'english', 'hindi', 'tamil')
        limit: Maximum number of results to return (default: 20)
    """
    try:
        # First get all programs from the country
        params = {
            "option": "com_program",
            "Itemid": 250,
            "Submit": "Filter",
            "task": "filter",
            "program": 0,
            "cat": 0,
            "utm_medium": "yogalanding",
            "utm_content": "pgmspanel",
            "date": 0,
            "event": 0,
            "format": "json",
            "rejuvenation": 0,
            "utm_source": "mcp",
            "utm_campaign": "sgapp",
            "search": "fuzzy",
            "count": 100,
            "radius": "",
            "startrec": 0,
            "category": "",
            "latlong": "",
            "city": "",
            "country": country,
            "v": 2,
        }
        
        response = await http_client.get(SCHEDULE_API_BASE, params=params)
        response.raise_for_status()
        programs = extract_programs(response.json())
        
        # Apply filters
        filtered_programs = []
        for program in programs:
            if online is not None:
                is_online = program.get('is_online') == "1"
                if is_online != online:
                    continue
            
            if with_sadhguru is not None:
                has_sadhguru = program.get('is_sadhguru') == "1"
                if has_sadhguru != with_sadhguru:
                    continue
            
            if language:
                program_lang = program.get('language', '').lower()
                if language.lower() not in program_lang:
                    continue
            
            filtered_programs.append(program)
            
            if len(filtered_programs) >= limit:
                break
        
        if not filtered_programs:
            return f"No programs found matching the specified filters in {country}."
        
        formatted_programs = "\n---\n\n".join(
            format_program(program, idx + 1) for idx, program in enumerate(filtered_programs)
        )
        
        return f"Found {len(filtered_programs)} filtered programs in {country}:\n\n{formatted_programs}"
    
    except Exception as e:
        return f"Error filtering programs: {str(e)}"


@mcp.tool()
async def get_available_countries() -> str:
    """
    Get a list of all countries where Isha Foundation programs are available.
    Use this to help users discover locations.
    """
    try:
        params = {
            "option": "com_program",
            "itemid": 250,
            "task": "list",
            "country": 1,
            "city": 0,
        }
        
        response = await http_client.get(ISHA_API_BASE, params=params)
        response.raise_for_status()
        countries = response.json()
        
        country_list = "\n".join(f"- {value}" for value in countries.values())
        
        return f"Available Countries:\n\n{country_list}"
    
    except Exception as e:
        return f"Error fetching countries: {str(e)}"


@mcp.tool()
async def get_cities_in_country(country: str) -> str:
    """
    Get a list of cities in a specific country where Isha Foundation programs are available.
    
    Args:
        country: Country name
    """
    try:
        params = {
            "option": "com_program",
            "itemid": 250,
            "task": "list",
            "city": 1,
            "country": country,
        }
        
        response = await http_client.get(ISHA_API_BASE, params=params)
        response.raise_for_status()
        cities = response.json()
        
        city_list = "\n".join(f"- {value}" for value in cities.values())
        
        return f"Cities in {country}:\n\n{city_list}"
    
    except Exception as e:
        return f"Error fetching cities: {str(e)}"


@mcp.tool()
async def list_program_categories() -> str:
    """
    Get a list of all available program categories and their keywords.
    Use this to help users understand what types of programs are available.
    """
    category_list = "\n\n".join(
        f"**{cat['name']}** (ID: {cat['category_id']})\nKeywords: {', '.join(cat['keywords'])}"
        for cat in PROGRAM_CATEGORIES
    )
    
    return f"Available Program Categories:\n\n{category_list}"


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()


