/*
📊 Data Exploration in SQL — COVID-19 Cases, Deaths & Vaccinations
Overview
Exploratory analysis of the COVID-19 deaths and vaccinations datasets in SQL Server to understand infection rates, mortality, regional differences, and vaccination progress. 
The work prepares clean, queryable outputs for BI tools (Power BI/Tableau) and demonstrates practical SQL for analytics.

What I did
Profiled core fields (location, date, total_cases, new_cases, total_deaths, population).
Case fatality analysis: total_deaths / total_cases * 100 to estimate mortality risk (country-level and over time).
Infection penetration: total_cases / population * 100 to measure % of population infected; identified highest infection rates by country.
Severity ranking: Calculated max death counts and continent-level totals to compare regional impact.
Global trendlines: Aggregated new_cases and new_deaths by date to track worldwide surges and the global death percentage over time.
Vaccination progress: Joined Deaths and Vaccinations by location+date and built a rolling cumulative sum of new_vaccinations using a window function to approximate % population vaccinated.

Reusable assets:
Built a CTE for readability and step-wise derivations.
Created a temp table for quick ad-hoc exploration.
Published a view (PercentPopulationVaccinated) for downstream visualisations.
Data hygiene: Filtered out non-country aggregates (continent IS NOT NULL) and handled type issues with explicit CAST/CONVERT.

Techniques & SQL Concepts
JOINs, GROUP BY aggregates, window functions (ROW_NUMBER, SUM() OVER (PARTITION BY … ORDER BY …)), CTEs, temp tables, views, type conversions, date-wise rollups, and ranking.

Outcome
Produced queryable tables/views that surface:
% population infected and case fatality by country/continent
Countries with highest infection rates and highest deaths
Global daily trendlines for cases and deaths
Cumulative vaccinations and % of population vaccinated over time
These outputs feed cleanly into BI dashboards for monitoring spread, severity, and vaccination impact.
*/
Select *
From PortfolioProject..CovidDeaths
where continent is not null
Order by 3,4


--Select *
--From PortfolioProject..CovidVaccinations
--Order by 3,4

--Select Data that we are using

Select location,date, total_cases, new_cases, total_deaths, population
From PortfolioProject..CovidDeaths
Order by 1,2

--Total Cases Vs Total Deaths
--Shows likelihood of dying if you contract covid by countries
Select location,date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where location like '%India%'
Order by 1,2

-- Looking at Total Cases vs Population
-- Shows what percentage of population got Covid
Select location,date, population, total_cases,  (total_cases/population)*100 as PercentPopulationInfected
From PortfolioProject..CovidDeaths
Where location like '%India%'
Order by 1,2

--what country has the highest infection rate compared to the population
Select location, population,MAX(total_cases) as HighestInfectionCount,  MAX((total_cases/population))*100 as PercentPopulationInfected
From PortfolioProject..CovidDeaths
where continent is not null
Group by location, population
Order by PercentPopulationInfected desc

--Highest Death count by countries population
Select location, MAX(cast(total_deaths as int)) as TotalDeathCount -- converting varchar to int
From PortfolioProject..CovidDeaths
where continent is not null
Group by location
Order by TotalDeathCount desc


--showing the continents with highest death count per population
Select continent, MAX(cast(total_deaths as int)) as TotalDeathCount -- converting varchar to int
From PortfolioProject..CovidDeaths
where continent is not null
Group by continent
Order by TotalDeathCount desc
--Testing it will continent is null
--Select location, MAX(cast(total_deaths as int)) as TotalDeathCount -- converting varchar to int
--From PortfolioProject..CovidDeaths
--where continent is null
--Group by location
--Order by TotalDeathCount desc


--Global numbers
Select date, SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where continent is not null
Group by date
order by 1,2

--Global numbers without date
Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where continent is not null
order by 1,2

--Combining two tables covid deaths and covid vaccinations
--Looking at total population vs vaccinations
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

--More details
--Parition breaks the sum based on new locations
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(Convert(int, vac.new_vaccinations)) 
OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

--Use CTE 
With PopvsVac (Continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
as 
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(Convert(int, vac.new_vaccinations)) 
OVER (Partition by dea.location Order by dea.location, 
dea.date) as RollingPeopleVaccinated --,(RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)
Select *, (RollingPeopleVaccinated/population)*100
From PopvsVac


--TEMP Table

DROP Table if exists #PercentPopulationVaccinated --to delete temp table automatically
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
location nvarchar(255),
Date datetime,
Population numeric, 
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)
Insert into #PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(Convert(bigint, vac.new_vaccinations)) --bigint to avoid overflow
OVER (Partition by dea.location Order by dea.location, 
dea.date) as RollingPeopleVaccinated --,(RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null
--order by 2,3

Select *, (RollingPeopleVaccinated/population)*100
From #PercentPopulationVaccinated


--Creating a view to store data for later visulizations
Create View PercentPopulationVaccinated as 
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(Convert(bigint, vac.new_vaccinations)) --bigint to avoid overflow
OVER (Partition by dea.location Order by dea.location, 
dea.date) as RollingPeopleVaccinated
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3

DROP VIEW IF EXISTS PercentPopulationVaccinated;

CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population,
       vac.new_vaccinations,
       SUM(CONVERT(BIGINT, vac.new_vaccinations)) OVER (
           PARTITION BY dea.location 
           ORDER BY dea.location, dea.date
       ) AS RollingPeopleVaccinated
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
    ON dea.location = vac.location 
    AND dea.date = vac.date
WHERE dea.continent IS NOT NULL;

-- to resolve when i cant see file under view
EXEC sp_help 'PercentPopulationVaccinated';

SELECT * FROM PercentPopulationVaccinated; -- to view everything from table

SELECT name, SCHEMA_NAME(schema_id) AS schema_name
FROM sys.views
WHERE name = 'PercentPopulationVaccinated';

