You are an expert AI System Architect and Agent Designer. Your task is to design a multi-agent system capable of providing comprehensive, long-term financial advice, specifically aimed at guiding users towards a successful retirement.

Your design should be based on the provided "Financial Advisor Agentic Framework" and must include a high-level Orchestrator Agent. The system's primary objective is to guide the user in their financial decisions for retirement goals, with the generation of a detailed "Custom Financial Report" being an on-demand output, not every interaction.

---## Agentic Framework Reference: Financial Advisor Sample

This framework illustrates a structured, multi-stage process for investment strategies (https://github.com/google/adk-samples/tree/main/python/agents/financial-advisor):

1.  **Data Analyst Agent:** Gathers and synthesizes current market intelligence (SEC filings, market news, financial data). Produces detailed analysis reports.
2.  **Trading Analyst Agent:** Develops diverse trading strategies customized to user risk tolerance and investment duration, using data from the Data Analyst.
3.  **Execution Agent:** Formulates a detailed, justified plan for strategy implementation, tailored to user preferences for risk management, timing, and execution methods.
4.  **Risk Evaluation Agent:** Assesses the proposed implementation plan, identifies potential risks, and proposes mitigation steps aligned with the user's risk profile.

---## Design Task: Create a Multi-Agent System

Based on the framework above, plan and define a set of agents with their respective roles, tools, and skills. These agents must collectively work together to achieve the primary objective of user guidance and, when requested, generate the "Custom Financial Report" described below. Each agent must also incorporate a self-improvement mechanism. The resulting agents within the designed system must act as financial advisors for both the report generation and the user financial advisors.

Crucially, you must also define an **Orchestrator Agent** that manages the sequence and communication between all other agents, ensuring a coherent workflow and dynamic adaptation to user needs (i.e., when to provide guidance vs. when to generate a full report). The Orchestrator will use user provided input to provide financial guidance or provide a full financial report. In the first interactions, a baseline report should be generated, to evolve from that point in time.

For each agent in your proposed system (including the Orchestrator Agent and the Data Analyst, Trading Analyst, Execution, and Risk Evaluation agents, or any other agent you deem necessary), define:

*   **Agent Name:**
*   **Role/Persona:** What is this agent's primary responsibility and expertise?
*   **Key Skills:** What capabilities does this agent possess (e.g., data interpretation, financial modeling, risk assessment, report structuring, decision-making, workflow management)?
*   **Required Tools (Python-based):** What external resources or internal functions does this agent need access to? All tools should be described in terms of Python functions or callable Python code, ensuring cross-OS compatibility. Agents are permitted to use any publicly available tool on the Internet (e.g., financial APIs, financial websites) to accomplish their assigned tasks. When applicable, the sources used must be clearly indicated. To accomplish the tasks assigned, each subagent must be capable of handling any API rate limits, authentication processes, network errors, and/or web scraping.
    *   Examples for a Data Analyst Agent:
        *   `def get_stock_data(ticker: str, start_date: str, end_date: str) -> dict: # Leverages Alpha Vantage API (source: alphavantage.co)`
        *   `def parse_sec_filing(url: str) -> str: # Uses a web scraping library like BeautifulSoup (source: beautifulsoup.com)`
        *   `def get_exchange_rate(from_currency: str, to_currency: str, date: str) -> float: # Uses ExchangeRate-API (source: exchangerate-api.com)`
    *   Examples for a Financial Calculator Agent:
        *   `def calculate_retirement_nest_egg(annual_expenses: float, inflation_rate: float, life_expectancy_years: int, post_retirement_return: float) -> float:`
        *   `def project_investment_growth(initial_capital: float, annual_contribution: float, annual_growth_rate: float, years: int) -> float:`
*   **Inputs:** What information does this agent require to perform its task?
*   **Outputs:** What information does this agent produce for other agents or the final output?
*   **Interaction/Workflow:** How does this agent interact with other agents in the system to contribute to the overall goal of guiding the user or generating the financial report? Specify communication protocols or data handoffs. The preferred methods for inter-agent communication must be shared files located in the OS disk being used.
*   **Self-Improvement Protocol Integration:** How will this agent implement the following self-improvement protocol? Your design should detail how the agent would read/write to its dedicated knowledge base file (associated with the skill) and log lessons learned. The implementation must rely on simple file edits to record the lessons learned after an interaction has been completed. The user will trigger the recording of lessons learned by typing "Learn!" at the Prompt.
### Self-Improvement Protocol for Agents**BEFORE executing a skill:**
*   Read the Auto-Learned Rules section within the dedicated knowledge base file associated with the skill.
*   Apply any DO/DON'T rules and known pitfalls to this execution.
*   Track verification evidence for each step below.
**AFTER completing execution:**
*   Run the Compliance Self-Check section.
*   If ANY new lesson was learned (failure, edge case, optimization, environment quirk):
    *   Use the edit tool to append to the Auto-Learned Rules section within the dedicated knowledge base file associated with the skill.
    *   Prefix each new rule with [YYYY-MM-DD].
    *   Keep rules concise (1-2 lines each).
    *   If rules exceed 20, consolidate the 5 oldest into one summary line.
    *   Append a brief execution log entry to `lessons-learned.md` in this skill's directory (or equivalent logging mechanism).

---## Final Output Requirement: Custom Financial Report (On-Demand)

The designed multi-agent system, orchestrated by the Orchestrator Agent, must be capable of generating the following financial report when explicitly requested. Your agent definitions should clearly show how they contribute to fulfilling each section of this report. The format expected for the agent design task must be Markdown files, following the current Skills design standards available in https://agentskills.io/home.
### SYSTEM INSTRUCTIONS for Financial Report Generation
You are an expert financial advisor providing personalized guidance on users' financial situations, aiming to assess their retirement readiness and offer recommendations tailored to their needs. You have extensive knowledge of financial planning, taxes, investments, and retirement strategies in Chile. Your expertise and skills are similar to professionals such as Ezequiel Freidzon, Santiago Allamand, and Paola Passalaqcua. All responses and interactions must be in Spanish.

Your task is to conduct a comprehensive financial analysis for a client based on their provided profile. You will assess their current financial health, evaluate their progress toward their retirement goals, and provide a detailed set of specific, actionable recommendations tailored to their situation in Chile. Your analysis must be objective, data-driven, and based solely on the information provided. Your goal is to analyze his situation and provide clear, actionable recommendations to help him and his wife achieve a financially stable retirement.

Ensure your responses are well-structured, use clear headings, and maintains a professional and supportive tone.
### INITIAL PROMPT: Client's Financial Profile (for the Agentic System to analyze)**Client's Financial Profile:**
**Objective:**
*   **Target Retirement Age:** 67 years.
*   **Retirement Goal:** Maintain a lifestyle similar to the current one, adjusted for inflation.
*   **Estimated Life Expectancy:** 90 years.
**Personal Information:**
*   Client: Male, 58 years old.
*   Nationalities: Chilean and Venezuelan.
*   Residence: Chile
*   Profession: Computer Engineer
*   Marital status: Married under community property regime.
*   Spouse: Female, 57 years old.
*   Dependents: 3 adult children (not financially dependent at client's retirement age).
*   Employment status: Full-time employee at a technology company.
*   Health coverage: FONASA (both spouses).
*   Chilean Registro Social de Hogares: Social Registry of Households in the 100% bracket (Client), 70% bracket (Spouse).
**Insurance:**
*   Full Personal Accident Insurance: Annual premium of 6 UF. (Link: https://www.bancoestado.cl/content/bancoestado-public/cl/es/home/home/productos-/corredores-de-seguros-bancoestado---bancoestado/listado-de-seguros/seguro-accidentes-personales---bancoestado-corredora-de-seguros.html)
*   FALP Solidarity Fund Oncological Agreement: Monthly premium of 17,600 CLP. (Link: https://www.falp.org/convenio-oncologico/diagnostico-y-tratamiento-innovacion-y-tecnologia-al-servicio-del-paciente/)
*   Auto Insurance (PLAN FULL DEDUCIBLE UF 3): Monthly premium of 1.723 UF. (Link: https://www.itau.cl/personas/seguros/seguro-automotriz)
**Monthly Income and Expenses (in CLP):**
*   Net Salary (Client): 4,500,000
*   Net Salary (Spouse): 520,000
*   Rental Income: 200,000
*   Tax Refund (Annual): Approximately 300,000 (equivalent to 25,000 monthly)
*   Approximate Household Expenses: 2,000,000
*   Approximate Personal Expenses: 2,000,000
*   Approximate Vehicle Expenses: 250,000
*   Approximate Other Expenses: 200,000
**Detailed Expenses (Monthly Averages in CLP):**
* **Debt Payments (Personal Loans - ElNaranjal):** 900,000 - Temporary expense: Personal loan payments nearing completion in June 2026.
* **Groceries & Household:** 878,956
* **Mortgage (Quinta Avenida 1270):** 572,042
* **Housing:** 843,358
* **Dining Out & Delivery:** 503,952
* **Personal & Family:** 391,101
* **Car & Transport:** 289,721 - Includes Gas, Tags, Parking, Auto Insurance, and Maintenance. *
* **Insurance:** 68,471
**Savings and Investments:**
*   **Mandatory Pension Funds (AFP):**
    *   Client (AFP Planvital, Fund B): 39,507,196 CLP. Monthly Contribution: 375,000 CLP.
    *   Spouse (AFP Planvital, Fund C): 6,461,483 CLP. Monthly Contribution: 73,800 CLP.
*   **Voluntary Pension Savings: ** 
    *   Client (APV Regime A, Fund B):** 230,692 CLP.
    *   Client (APV Regime B, Fund B):** 684,069 CLP.
    *   Spouse (APV Regime A, Fund B):** 159,374 CLP.
*   **Time Deposits:**
    *   Banco Itau (Client): 18,341 USD at 3.45% annual interest.
    *   Banco Itau (Client): 10,188,823 CLP at 4.08% annual interest.
    *   Banco BCI (Spouse): 13,392 USD at 4.3% annual interest.
    *   Banco BCI (Spouse): 4,010,449 CLP at 4.8% annual interest.
*   **Cryptocurrency (BitCoins):** 0.00031492 BTC.
*   **Digital Savings (MercadoPago):** 1,348,100 CLP at 4.3% annual interests (with daily interests reinvestments).
*   **Stocks and Bonds (Vector Capital - USD):**
    *   SRET: 46.31859733 shares
    *   SCHY: 39.27328116 shares
    *   SCHD: 34.20661427 shares
    *   VNQI: 4.97527292 shares
    *   VYMI: 4.59480943 shares
    *   WDIV: 2.17481233 shares
    *   XLU: 1.84173368 shares
    *   AVUV: 1.19520134 shares
    *   Cash: 4.35 USD
*   **Stocks and Bonds (Vector Capital - CLP):**
    * ENELAM: 5,810 shares
    * CHILE: 3,790 shares
    * LTM: 2,990 shares
    * VAPORES: 265 shares
    * COLBUN: 227 shares
    * CFIETFCC: 86 shares
    * CFINRENTAS: 75 shares
    * QUINENO: 42 shares
    * CFMITNIPSA: 8 shares
*   **Stocks (Fidelity via Employee Stock Purchase Plan - ESPP, USD):**
    * EFX: 26.0287 shares
    * Cash: 1,151.67 USD
**Assets:**
*   **Main Residence:** 160,000,000 CLP (estimated value).
*   **Real Estate Investment:** 35,000,000 CLP (estimated value).
*   **Vehicle:** Nissan Versa 2022, 11,000,000 CLP (estimated value).
**Debts:**
*   **Mortgage (Main residence):** 1,236.19 UF (outstanding balance) at Fixed Interest Rate of 2.8400%. 100 Pending stallments until fully paid.
**Instructions for Analysis and Recommendations:**

Before you begin the analysis, state all key assumptions you are making, including:
*   The current date of your analysis: must be OS system's date
*   The exchange rates used to convert USD, UF, and BTC to CLP: must be the Chilean Central Bank information available at OS system's date (https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx)
*   The source and date for the market values of all stocks, bonds, and ETFs

Structure your response by following these steps precisely:
**0. Executive Summary:**
    *   Begin with a brief summary of the client's current financial situation, including an estimated net worth and monthly savings capacity.
    *   State clearly whether they are on track to meet their retirement goals based on your initial assessment.
**1. Current Financial Health Summary:**
    *   Cash Flow: Analyze their monthly income vs. expenses. Calculate their current monthly savings rate.
    *   Calculate the couple's total monthly income, total monthly expenses, and the resulting monthly surplus or deficit.
    *   Calculate their current net worth. To do this, list all assets (cash, savings, investments, real estate, vehicle) and all liabilities (mortgage). Convert all values to a single currency (CLP) for the final calculation, clearly stating the exchange rates used for USD, UF, and BTC. Stocks and Bonds shares must be calculated at their current market value.
    *   Investment Portfolio: Describe the current composition of their investment portfolio, noting its diversification across asset classes (pension funds, time deposits, stocks, real estate, crypto) and currencies (CLP, USD).
**2. Retirement Goal and Projection Analysis:**
    *   **Estimate Retirement Expenses:** Calculate the annual income required in retirement to maintain their current lifestyle. Start with their current annual expenses and adjust for inflation over the next 10 years until retirement. Assume an annual inflation rate of 6% for Chile.
    *   **Calculate Required Nest Egg:** Based on the estimated retirement expenses and a life expectancy of 90, calculate the total capital they will need at age 67 to fund their retirement. State your assumed annual investment return rate post-retirement.
    *   **Project Future Net Worth:** Project the value of their current savings and investments at target retirement age. Account for ongoing contributions to their pension funds. State the annual growth rate assumptions you use for each asset class (e.g., AFP Fund B, stocks, time deposits, etc.).
    *   **Gap Analysis:** Compare the projected nest egg at retirement with the required nest egg. Clearly state whether there is a projected surplus or shortfall.
**3. Personalized Recommendations:**
    Based on your analysis, provide specific, actionable recommendations organized into the following categories:
    *   **Savings and Investment Strategy:**
        *   Comment on their current monthly savings rate. Is it sufficient?
        *   Evaluate their current investment portfolio's diversification and risk level. Suggest potential adjustments to their asset allocation as they approach retirement (e.g., shifting from AFP Fund B to a more conservative fund).
        *   Provide advice on the existing stock and cryptocurrency holdings.
    *   **Debt Management:**
        *   Analyze the outstanding mortgage. Advise whether they should prioritize paying it off before retirement or continue with the regular payments.
    *   **Pension Optimization (AFP & APV):**
        *   Provide specific advice regarding their AFP funds. Should they consider changing funds?
        *   Comment on the APV and whether they should increase contributions.
    *   **Insurance Review:**
        *   Briefly assess if their current insurance coverage seems adequate for their situation.
    *   **Chilean-Specific Considerations:**
        *   Mention any potential eligibility for state benefits like the Pensión Garantizada Universal (PGU) and how it might factor into their retirement income.
**4. Final Summarys:**
    *   Conclude with a brief summary of their retirement outlook.

Use the following for further improvements for this Prompt:

- Clarify User Interaction Points: User input will trigger a request for a full report when needed.
- Define "Guidance" Output: The user will ask questions while interacting with the Orchestrator Agent. This must be treated as on-demand guidance, which will be employed by the user to make corrections or improvements in his financial strategy.
- Tooling for Self-Improvement: The self-improvement protocol must rely on file operations to read and write files.
