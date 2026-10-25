from typing import List, Dict, Any

INTERNAL_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "doc_id": "DOC-SOP-04",
        "title": "SOP-04: Cold Chain Storage and Temperature Control Guidelines",
        "department": "Quality Assurance & Logistics",
        "document_date": "2024-01-15",
        "access_level": "internal",
        "sections": [
            {
                "section": "1.0 Purpose and Scope",
                "content": "This Standard Operating Procedure defines mandatory temperature thresholds for all perishable food items handled across FreshRoute Foods warehouses and transit fleet."
            },
            {
                "section": "2.0 Temperature Classifications",
                "content": "Category A (Dairy Products - Milk, Paneer, Yogurt): Must be maintained strictly between +2°C and +4°C at all times. Any excursion above +6°C lasting more than 4 consecutive hours requires mandatory spoilage write-off and laboratory microbiological clearance before release.\nCategory B (Fresh Produce - Cucumbers, Leafy Greens): Storage temp +2°C to +8°C.\nCategory C (Frozen Foods): Storage temp -18°C or lower."
            },
            {
                "section": "3.0 Transit Breach Protocol",
                "content": "If a refrigerated reefer vehicle incurs transit delays exceeding 6 hours, the driver must activate auxiliary diesel refrigeration units. In case of primary reefer failure or diesel exhaustion leading to cab temperatures exceeding 10°C, the logistics dispatcher must log a formal 'Cold Chain Breach Incident' and divert the shipment to the nearest certified cold storage depot."
            }
        ]
    },
    {
        "doc_id": "DOC-INC-2024-08",
        "title": "Incident Investigation Report: Delhi Central DC Chiller Compressor Outage",
        "department": "Warehouse Engineering & Maintenance",
        "document_date": "2024-08-18",
        "access_level": "internal",
        "sections": [
            {
                "section": "1.0 Executive Summary",
                "content": "Between August 11, 2024 and August 16, 2024, the primary Bitzer screw compressor unit serving Cold Room #2 at Delhi Central Distribution Centre (WH-DEL-01) suffered catastrophic stator coil failure. The automated backup generator failed to switch power to the auxiliary reciprocating compressor due to a corroded contactor relay."
            },
            {
                "section": "2.0 Temperature Excursion and Stock Loss",
                "content": "Ambient temperature in Cold Room #2 rose from 3.2°C to a peak of 16.8°C over 48 hours. Inventory on hand—primarily Fresh Organic Paneer 500g (Batch PN-2408), Pasteurized Milk, and Fresh Poultry—exceeded critical bacterial growth safety limits. In compliance with SOP-04, 18,400 units representing a total inventory write-off value of ₹26.85 Lakhs were condemned and incinerated."
            },
            {
                "section": "3.0 Corrective and Preventive Actions (CAPA)",
                "content": "1. Immediate replacement of dual contactor switch relays.\n2. Procurement of an N+1 secondary chiller unit by Q4 2024.\n3. Installation of IoT cloud-connected independent temperature loggers with SMS/escalation alarms to the VP of Operations."
            }
        ]
    },
    {
        "doc_id": "DOC-SLA-CARRIER-24",
        "title": "Master Carrier Service Level Agreement: North Indian Logistics Corridors",
        "department": "Supply Chain & Procurement",
        "document_date": "2024-03-01",
        "access_level": "internal",
        "sections": [
            {
                "section": "Section 4: Transit Time and Delay Penalties",
                "content": "Contracted carriers on Delhi-Chandigarh (RT-DEL-CHD) and Delhi-Jaipur (RT-DEL-JAI) corridors must deliver shipments within 6.0 hours of dispatch. Delays beyond 3.0 hours incur a 15% freight penalty per hour, up to 100% of freight value."
            },
            {
                "section": "Section 7: Force Majeure & Severe Weather Exceptions",
                "content": "Carriers are exempt from liquidated damages if delay is directly attributable to government-declared national highway closures or extreme weather (defined as precipitation > 75mm/day causing official road closure by NHAI). However, the carrier remains 100% liable for cargo spoilage resulting from unmaintained reefer units or driver negligence in refilling refrigeration diesel."
            }
        ]
    },
    {
        "doc_id": "DOC-REP-Q3-NORTH",
        "title": "Quarterly Business Review: North India Region Q3 2024 Performance",
        "department": "Regional Sales & Operations",
        "document_date": "2024-10-05",
        "access_level": "internal",
        "sections": [
            {
                "section": "1.0 Financial Headwinds Summary",
                "content": "North India experienced a sharp profitability compression in Q3 2024, led by an unprecedented operating loss in August 2024 (net margin -29.52%). Total revenue declined by 16% MoM to ₹1.85 Cr due to stockouts and order cancellations."
            },
            {
                "section": "2.0 Root Cause Analysis",
                "content": "The August contraction was driven by two simultaneous compounding events:\n1. Severe monsoon rains across Haryana, Punjab, and Rajasthan resulting in NH-44 highway waterlogging and average delivery delays of 18-38 hours, causing ₹11.9 Lakhs of transit spoilage and ₹18.5 Lakhs in surge freight costs.\n2. Catastrophic chiller compressor failure at Delhi Central DC (WH-DEL-01) destroying ₹26.85 Lakhs of dairy stock."
            },
            {
                "section": "3.0 Product Margin Trends",
                "content": "Fresh Organic Paneer 500g saw strong promotional volume growth (+40%), but gross margins fell from 28% to 8.5% due to a 20% discount combined with an 18% surge in farm milk procurement costs in Punjab dairies."
            }
        ]
    },
    {
        "doc_id": "DOC-MEET-EXEC-2408",
        "title": "Executive Committee Minutes: Emergency Operations Meeting (Aug 15, 2024)",
        "department": "Executive Leadership",
        "document_date": "2024-08-15",
        "access_level": "confidential",
        "sections": [
            {
                "section": "Discussion Points",
                "content": "CEO and COO reviewed the simultaneous highway disruption on NH44 and the chiller breakdown at Delhi DC. Approved emergency fund allocation of ₹25 Lakhs for temporary refrigerated container leasing and authorized immediate air-freight transport for critical quick-commerce customer fulfillments."
            }
        ]
    }
]
