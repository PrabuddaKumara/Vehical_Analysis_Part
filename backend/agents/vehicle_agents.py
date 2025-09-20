try:
    from crewai import Agent, Task, Crew
except ImportError:
    print("CrewAI not properly installed, using mock classes")
    class Agent:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class Task:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class Crew:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

from tools.custom_tools import SriLankanVehicleScraperTool, AdDetailsExtractorTool, WebSearchTool

class VehicleAgents:
    def __init__(self):
        self.web_search_tool = WebSearchTool()
        self.scraper_tool = SriLankanVehicleScraperTool()
        self.extractor_tool = AdDetailsExtractorTool()
        print("VehicleAgents initialized successfully")
    
    def vehicle_comparison_agent(self):
        return Agent(
            role='Expert Vehicle Comparison Analyst',
            goal='Provide comprehensive comparisons between two vehicle models including specifications, pros/cons, and expert opinions',
            backstory='''You are a seasoned automotive expert with years of experience in vehicle analysis. 
                        You specialize in comparing different vehicle models by analyzing their technical specifications, 
                        reliability ratings, fuel efficiency, maintenance costs, and overall value proposition.
                        You present information in a clear, structured format that helps consumers make informed decisions.''',
            tools=[self.web_search_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def sri_lankan_ad_finder_agent(self):
        return Agent(
            role='Sri Lankan Vehicle Advertisement Specialist',
            goal='Find active vehicle listings on popular Sri Lankan automotive websites',
            backstory='''You are an expert in the Sri Lankan automotive market with deep knowledge of 
                        local vehicle trading platforms like ikman.lk, riyasewana.com, and patpat.lk.
                        You excel at finding relevant vehicle advertisements and identifying genuine listings
                        that match specific vehicle models requested by users.''',
            tools=[self.scraper_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def ad_details_extractor_agent(self):
        return Agent(
            role='Advertisement Data Extraction Expert',
            goal='Extract structured and accurate information from vehicle advertisements',
            backstory='''You are a specialist in extracting key information from online advertisements.
                        You can quickly identify and extract important details like price, year of manufacture,
                        mileage, location, and other specifications from vehicle listings across different websites.
                        You ensure data accuracy and format consistency in your extractions.''',
            tools=[self.extractor_tool],
            verbose=True,
            allow_delegation=False
        )

class VehicleTasks:
    def comparison_task(self, agent, vehicle1, vehicle2):
        return Task(
            description=f'''
            Perform a comprehensive comparison between {vehicle1} and {vehicle2}.
            
            Your analysis should include:
            1. Technical specifications (engine, fuel efficiency, dimensions)
            2. Reliability and safety ratings
            3. Pros and cons for each vehicle
            4. Price range and value proposition
            5. Maintenance and running costs
            6. User reviews and expert opinions
            
            Format your response as a structured comparison that highlights key differences
            and similarities between the two vehicles. Make recommendations based on different
            use cases (city driving, family use, fuel economy, etc.).
            ''',
            agent=agent,
            expected_output='A detailed comparison report in structured format covering all requested aspects'
        )
    
    def ad_finding_task(self, agent, vehicle1, vehicle2):
        return Task(
            description=f'''
            Search for active vehicle advertisements for both {vehicle1} and {vehicle2} 
            on Sri Lankan automotive websites.
            
            Focus on:
            1. ikman.lk - the most popular platform
            2. riyasewana.com - automotive focused site  
            3. patpat.lk - general marketplace
            
            Find at least 3-5 relevant listings for each vehicle if available.
            Return the URLs of found advertisements.
            ''',
            agent=agent,
            expected_output='A list of URLs for vehicle advertisements found on Sri Lankan websites'
        )
    
    def extraction_task(self, agent, ad_urls):
        return Task(
            description=f'''
            Extract detailed information from each of the provided advertisement URLs.
            
            For each advertisement, extract:
            1. Title/Vehicle name
            2. Price (in LKR)
            3. Year of manufacture
            4. Mileage (in km)
            5. Location
            6. Brief description
            7. Original ad URL
            
            Handle cases where some information might not be available.
            Format the extracted data as structured JSON objects.
            
            Advertisement URLs to process: {ad_urls}
            ''',
            agent=agent,
            expected_output='Structured JSON data for each advertisement containing extracted vehicle details'
        )