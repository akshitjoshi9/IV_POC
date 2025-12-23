QUESTION_WISE_TEXT = {
    "What is the overarching regulation governing Clinical Trails in UK?": """
    ## Special Instruction:
    Try to return the first regulation and upcoming reforms
    
    ### Expected Answers:
    Expected: The overarching regulation for clinical trials in the UK is the Medicines for Human Use (Clinical Trials) Regulations 2004 (as amended), with upcoming reforms under the Medicines for Human Use (Clinical Trials) (Amendment) Regulations 2024 to be fully implemented by April 2026.
    """,

    "What is the name of the organisation that acts as the regulatory authority for clinical trials in the UK?": """
    ## Special Instruction:
    When answering this question, always prefer the information from the following URL:
    https://www.legislation.gov.uk/uksi/2004/1031/data.xht?view=snippet&wrap=true
    """,

    "What is the name(s) of the organisation(s) that act as the central ethics committee for clinical trials in the UK?": """
    
    ### Expected Answers:
    Expected: Research Ethics Committees (RECs), overseen by the Health Research Authority (HRA), conduct ethical reviews for clinical trials, with specific committees determined by trial location within a unified national ethics framework. These committees are recognized by the UK Ethics Committee Authority (UKECA). 
    
    """,

    "What category does the legislation fall under? Act, regulation, decree, order, etc": """
    
    ### Expected Answers:
    Expected: The Medicines for Human Use (Clinical Trials) Regulations 2004 falls under the category of regulation.
    
    ## Special Instruction:
    - Look at the legislation title in the context. 
    - You MUST repeat the full legislation title exactly as it appears in the context.
    
    """,

    "When was the UK clinical trials regulation published?": """
    
    ### Expected Answers:
    - Give the date of publication.
    - Give in Date Format: dd Month yyyy
    
    ## Special Instruction:
    When answering this question, always prefer the information from the following URL:
    https://www.legislation.gov.uk/uksi/2004/1031/data.xht?view=snippet&wrap=true
    """,

    "What types of clinical trials fall under the scope of the UK Medicines for Human Use (Clinical Trials) Regulations?": """
    ## Special Clinical Trials Rule
    - Only if the question is exactly:
        "What types of clinical trials fall under the scope of the UK Medicines for Human Use (Clinical Trials) Regulations?":
            - Search and return the regulation title (with Amendment + year).
            - Use the latest year’s regulation.
            - Answer format:
                "Medicines for Human Use (Clinical Trials) (Amendment) Regulations 2025 apply to Clinical Trials of Investigational Medicinal Products (CTIMPs)".
    """,

    "Are non-interventional or observational studies covered by the same regulations?": """
    ### Expected Answers:
    Expected: No.
    """,

    "How do UK clinical trial regulations distinguish between low-risk and high-risk studies?": """
    
    ### Expected Answers:
    Expected: New framework introduces risk-proportionate regulation, notification scheme for low risk trials
    
    ## Special Instruction:
    - When answering this question, always give to answer in one or two line as per the expected answer.
    """,

    "What are the legal responsibilities of a trial sponsor under UK law?": """
    
    ### Expected Answers:
    Expected: Legally responsible for compliance with regulations and GCP.
    
    """,

    "Can clinical trial sponsorship be shared between multiple organisations in the UK (e.g., co-sponsors or joint sponsors), and how is responsibility and liability managed in such arrangements?": """
    
    ### Expected Answers:
    Expected: Yes or No.
    """,

    "What are the requirements for a sponsor located outside the UK to conduct a clinical trial in the UK?": """
    ### Expected Answers:
    Expected: If sponsor not established in the UK they need to appoint a legal representative in the UK.
    """,

    "Is there a legal obligation to publish trial results, and within what timeframe?": """
    ### Expected Answers:
    Expected: Within 12 month of trial completion.
    """,

    "What are the new provisions for participant-facing summaries of trial results?": """
    
    ### Expected Answers:
    Expected: New provisions under the proposed UK clinical trials legislation will introduce a legal requirement to offer participant-facing summaries of trial results within 12 months of trial completion, in a plain language and suitable format, moving from current good practice to a mandatory legal obligation. 
    """,

    "What is the Combined Review process for clinical trials in the UK?": """
    
    ### Expected Answers:
    Expected: Single Application for MHRA and REC approval.
    
    """,

    "What are the legal timelines for approval from MHRA and Research Ethics Committees (RECs)?": """
    ### Expected Answers:
    Expected: 60 days plus 10 days for final decision.
    """,

    "How does the MHRA’s notification scheme work for initial clinical trial applications and subsequent amendments?": """
    
    ### Expected Answers:
    Expected: Simplifies approval for low-risk trials.
    
    ## Special Instruction:
    - Explicitly mention "low-risk" or "lower risk trials" when discussing the Notification Scheme.
    - Always answer based on the "New Notification Scheme" section from the context, if available.
    - If the answer cannot be found in the context, say: "I could not find this information in the provided documents."
    
    """,

    "Do UK regulations align with international standards such as ICH-GCP E6?": """
    ### Expected Answers:
    Expected: Yes, UK clinical trials regulations are being updated to align closely with international standards, particularly ICH-GCP E6 (R3). New regulations become effective, fully aligning UK clinical trial law with ICH-GCP E6 (R3).
    
    ## Special Instruction:
    - When answering this question, always base the response on MHRA’s consultation on ICH Good Clinical Practice Guideline (ICH E6(R3)).
    - If the retrieved documents contain this consultation, cite it explicitly in your answer.
    - Do not say "consult MHRA publications" — instead, extract details from the consultation text.
    """,

    "When does/did the updatedUK clinical trials regulation become effective?": """
    
    ## Special Instruction:
    - If the date was changed, then always return the latest date.
    
    ### Expected Answers:
    Expected: The new Medicines for Human Use (Clinical Trials) Regulations 2024 will take full effect on 28 Apr 2026, following a 12-month implementation period that began on 28 Apr 2025
    """,

    "What type of aggregate safety reporting is required by the UK regulatory authority and ethics committee for clinical trials? For example, DSUR, executive summary, ASR etc?": """
    ## Special Instruction:
    - Just return the type of periodic reporting.
    """,

    "What is the frequency for submitting aggregate safety reports during clinical trials in the UK?": """
    
    ### Expected Answers:
    Expected: DSUR (Development Safety Update Report) – required annually for CTIMPs
    
    ## Special Instruction:
    - Keep it simple and short.
    """,

    "What format should aggregate safety reports follow for clinical trials in the UK?": """
    
    ### Expected Answers:
    Expected: DSURs follow ICH E2F format
    
    ## Special Instruction:
    - Just return the format.
    """,

    "What is the preferred method for submitting aggregate reports to the UK Regulatory Authority and Ethics Committees?": """
    
    ### Expected Answers:
    Expected: 
    Clinical trials approved through the non-combined review process
    To Authority: You must submit your DSUR using MHRA Submissions via the Human Medicines Tile. Select ‘Development Safety Update Reports’ as the Regulatory Activity and ‘Original Submission’ from the Regulatory Sub Activity dropdown list.

    To REC (EC only applicable for approved studies not through the combined review): The report is usually submitted in PDF format via email or through an online portal designated by the EC or Research Ethics Committee (REC).
 
    Clinical trials approved through the combined review process
    IRAS (Integrated Research Application System): for combined review submissions
    """,

    "What is the preferred submission address for aggregate reports to the UK Regulatory Authority and Ethics Committees?": """
    
    ### Expected Answers:
    Expected: 
     - CT approved via non-combined review: to MHRA via MHRA Submission- https://mhrabpm.appiancloud.com/suite/sites/MHRA_Submissions (Medicines and E-cigarettes > Human Medicines > Dashboard > Under Regulatory Activity select "Development Safety Update Report), EC via email
     - CT approved via combined review: IRAS (https://id.nihr.ac.uk/authenticationendpoint/login.do?RelayState=9274bc93-02ea-44a5-b3d4-52211a6261a7&commonAuthCallerPath=%2Fsamlsso&forceAuth=true&passiveAuth=false&tenantDomain=carbon.super&sessionDataKey=6898e738-dc84-44a5-a0c8-f15d8a20c933&relyingParty=https%3A%2F%2Fhra-iras-prod1.pegacloud.net%3A443%2Fprweb%2Fsp%2F1544550718&type=samlsso&sp=HRA+-+IRAS&isSaaSApp=false&authenticators=GoogleOIDCAuthenticator%3AGoogle%3BAttributeBasedAuthenticator%3ALOCAL
    
    """,

    "Are there translation requirements for clinical trial aggregate reports prior to submission?": """
    
    ### Expected Answers:
    Expected: No translation required if submitted in English (the official language for UK regulatory bodies)
    
    """,

    "Are there any additional reports that must be submitted to the UK Regulatory Authority or Ethics Committees?": """
    
    ### Expected Answers:
    Expected: Yes. Urgent safety measures, protocol breaches, DHPC letters.
    
    ## Special Instruction:
    - The mandatory reports are: 
        - Urgent safety measures
        - Protocol breaches
        - Direct Healthcare Professional Communication (DHPC) letters
    - If the context mentions other reports in addition to these, include their names as well.
    - Do NOT include reports such as PSUR, PAR, or EU-only signal notifications unless the context explicitly states that they must be submitted to the UK Regulatory Authority or Ethics Committees.
    
    """,

    "Does REC require executive summary of DSUR?": """
    
    ### Expected Answers:
    Expected: Yes or No.
    
    """,

    "What are the regulatory requirements at the end of a clinical trial?": """
    
    ### Expected Answers:
    Expected: In detail answer
    
    """,

    "Are there differences in reporting for trials submitted via the combined review process?": """
    
    ### Expected Answers:
    Expected: Yes or No.
    
    """,

    "What are the requirements for reporting Urgent Safety Measures (USMs)?": """
    
    ### Expected Answers:
    Expected: In detail answer
    
    """,


    "Is there a requirement to submit domestic SUSARs to the UK Regulatory Authority and Ethics Committee?": """
    
    ### Expected Answers:
    Expected: 
        Yes. All SUSARs that occur in the UK must be reported to the MHRA. 
    """,

    "Is there a requirement to submit foreign SUSARs to the Authority/EC in UK?": """
    ### Expected Answers:
    Expected: Yes or No
    """,

    "What are the submission timelines for SUSAR reporting?": """
    ### Expected Answers:
    Expected:
        7-15 days
        7 calendar days for death/life-threatening cases. Any additional relevant information within 8 days of the initial report.
        15 calendar days for other serious criteria
    """,

    "What is the preferred submission method for SUSARs to the regulatory Authority and REC in the UK?": """
    
    ### Expected Answers:
    Expected:
        MHRA: Authority Portal or gateway
    """,

    "What is the required format for SUSAR submissions in UK?": """
    ### Expected Answers:
    Expected: E2B (R3)
    """,

    "Are there any translation requirements for SUSAR submissions?": """
    
    ### Expected Answers:
    Expected: No, If submitted in English
    """,

    "Who is responsible for submitting SUSAR reports to the UK regulatory authority and ethics committee?": """
    
    ### Expected Answers:
    Expected: Sponsor or a delegate such as CRO
    """,

    "What is the preferred submission address for SUSAR reports?": """
    
    ## Special Instruction:
    - Always give the answer ONLY from the latest guidance in the provided documents. 
    - The expected correct submission routes are:
        - ICSR Submissions (https://icsrsubmissions.mhra.gov.uk/login)
        - MHRA Gateway (https://assets.publishing.service.gov.uk/media/5fedc0b7d3bf7f0896806a28/URG_-_Registration_for_MHRA_Gateway.pdf)
    - Do NOT mention eSUSAR unless explicitly stated as still valid in the provided context.
    - Use bullet points to list the details for both MHRA and REC.
    - If the required information is not present in the context, say: "I could not find this information in the provided documents."
        
    ### Expected Answers:
    Expected: 
        - Report a SUSAR to the MHRA in one of the following ways:
            - Using ICSR Submissions (https://icsrsubmissions.mhra.gov.uk/login), which replaces the EudraVigilance website (EVWEB). The ICSR submissions route is used to submit single reports.
            - Using the MHRA Gateway (https://assets.publishing.service.gov.uk/media/5fedc0b7d3bf7f0896806a28/URG_-_Registration_for_MHRA_Gateway.pdf), which replaces the Eudravigilance Gateway. The Gateway route is used to submit single and bulk reports. To gain access to the MHRA Gateway you need to register to another portal called MHRA Submissions.
    """,

    "Is analysis of similar events required for reporting to UK regulatory authority and ethics committee?": """
    
    ### Expected Answers:
    Expected: No
    """,

    "Does the authority/EC want to receive cross reporting of SUSARs?": """
    
    ### Expected Answers:
    Expected: Yes.
    
    """,

    "Does the authority/EC want to receive unblinded SUSAR reports?": """
    
    ### Expected Answers:
    Expected: Yes.
    
    """,

    "Is there any requirement to submit SAEs to the UK authority/EC?": """
    
    ## Special Instruction:
        - Give the answer as per the given expected answers
    
    ### Expected Answers:
    Expected: No
    """,

}



QUESTION_WISE_RULES = {
    "Do UK regulations align with international standards such as ICH-GCP E6?": {
        "preferred_source_contains": [
            "ich"
        ]
    },
    # "What is the overarching regulation governing Clinical Trails in UK?": {
    #     "preferred_source_contains": [
    #         "uksi"
    #     ]
    # },
    # "What is the name(s) of the organisation(s) that act as the central ethics committee for clinical trials in the UK?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "authorisation-in-the-uk"
    #     ]
    # },

    "What category does the legislation fall under? Act, regulation, decree, order, etc": {
      "preferred_source_contains": [
            "uksi",
            "2004",
            "1031"
        ]
    },

    "When was the UK clinical trials regulation published?": {
        "preferred_source_contains": [
            "uksi",
            "2004",
            "1031"
        ]
    },
    "When does/did the updatedUK clinical trials regulation become effective?": {
        "preferred_source_contains": [
            "news",
            "clinical-trials-regulations",
            "signed"
        ]
    },
    "What types of clinical trials fall under the scope of the UK Medicines for Human Use (Clinical Trials) Regulations?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "authorisation-in-the-uk"
        ]
    },
    "How do UK clinical trial regulations distinguish between low-risk and high-risk studies?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "authorisation-in-the-uk"
        ]
    },
    "What are the requirements for a sponsor located outside the UK to conduct a clinical trial in the UK?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "apply",
            "for",
            "authorisation"
        ]
    },
    "Is there a legal obligation to publish trial results, and within what timeframe?": {
        "preferred_source_contains": [
            "www.gov.uk",
        ]
    },
    "What is the Combined Review process for clinical trials in the UK?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "authorisation-in-the-uk"
        ]
    },
    "What are the legal timelines for approval from MHRA and Research Ethics Committees (RECs)?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "approval-in-the-uk"
        ]
    },

    "How does the MHRA’s notification scheme work for initial clinical trial applications and subsequent amendments?": {
      "preferred_source_contains": [
          "www.gov.uk",
          "guidance",
          "authorisation-in-the-uk"
      ]
    },

    "What type of aggregate safety reporting is required by the UK regulatory authority and ethics committee for clinical trials? For example, DSUR, executive summary, ASR etc?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "What is the frequency for submitting aggregate safety reports during clinical trials in the UK?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "report-safety-issues"
        ]
    },
    "What format should aggregate safety reports follow for clinical trials in the UK?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "safety"
        ]
    },
    "What is the preferred method for submitting aggregate reports to the UK Regulatory Authority and Ethics Committees?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "report-safety-issues"
        ]
    },
    "What is the preferred submission address for aggregate reports to the UK Regulatory Authority and Ethics Committees?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "Who is responsible for submitting aggregate safety reports during a clinical trial?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "Are there translation requirements for clinical trial aggregate reports prior to submission?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    # "Are there any additional reports that must be submitted to the UK Regulatory Authority or Ethics Committees?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "reporting-of-safety"
    #     ]
    # },
    "Is there fee applicable for DSUR? Is there a cover letter required along with the DSUR?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "Does REC require executive summary of DSUR?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "What are the regulatory requirements at the end of a clinical trial?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "Are there differences in reporting for trials submitted via the combined review process?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "What is the role of the Reference Safety Information (RSI) in safety reporting?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },
    "What are the requirements for reporting Urgent Safety Measures (USMs)?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance"
        ]
    },

    "Is there a requirement to submit domestic SUSARs to the UK Regulatory Authority and Ethics Committee?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "clinical",
            "trial",
            "reporting",
            "safety",
            "events"
        ]
    },

    "Is there a requirement to submit foreign SUSARs to the Authority/EC in UK?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "clinical",
            "trial",
            "reporting",
            "safety",
            "events"
        ]
    },

    # "What are the submission timelines for SUSAR reporting?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "clinical",
    #         "trial",
    #         "safety",
    #         "reporting",
    #         "events"
    #     ]
    # },

    "What is the preferred submission method for SUSARs to the regulatory Authority and REC in the UK?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "clinical",
            "trial",
            "reporting",
            "safety",
            "events"
        ]
    },

    # "What is the required format for SUSAR submissions in UK?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "clinical",
    #         "trial",
    #         "safety",
    #         "reports"
    #     ]
    # },

    # "Are there any translation requirements for SUSAR submissions?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "clinical",
    #         "trial",
    #         "safety",
    #         "report",
    #         "issues"
    #     ]
    # },

    "Who is responsible for submitting SUSAR reports to the UK regulatory authority and ethics committee?": {
        "preferred_source_contains": [
            "www.gov.uk",
            "guidance",
            "clinical",
            "trial",
            "reporting",
            "safety",
            "events"
        ]
    },
    #
    # "What is the preferred submission address for SUSAR reports?": {
    #     "preferred_source_contains": [
    #     ]
    # },

    # "Is analysis of similar events required for reporting to UK regulatory authority and ethics committee?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "clinical",
    #         "trial",
    #         "safety",
    #         "reports"
    #     ]
    # },
    #
    # "Does the authority/EC want to receive cross reporting of SUSARs?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "clinical",
    #         "trial",
    #         "safety",
    #         "reports"
    #     ]
    # },
    #
    # "Does the authority/EC want to receive unblinded SUSAR reports?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "clinical",
    #         "trial",
    #         "safety",
    #         "reports"
    #     ]
    # },
    #
    # "Is there any requirement to submit SAEs to the UK authority/EC?": {
    #     "preferred_source_contains": [
    #         "www.gov.uk",
    #         "guidance",
    #         "clinical",
    #         "trial",
    #         "safety",
    #         "reports"
    #     ]
    # }
}