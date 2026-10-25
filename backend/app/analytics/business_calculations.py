from typing import Dict, Any, List, Optional
import math

class BusinessCalculationEngine:
    """
    Deterministic calculation and verification layer.
    Guarantees mathematical correctness without relying on LLM arithmetic.
    """

    @staticmethod
    def calculate_margin(numerator: float, denominator: float) -> float:
        """Calculates percentage margin: (numerator / denominator) * 100"""
        if not denominator or denominator == 0:
            return 0.0
        return round((numerator / denominator) * 100.0, 2)

    @staticmethod
    def calculate_growth_rate(current_val: float, baseline_val: float) -> Dict[str, Any]:
        """
        Calculates absolute delta and percentage change between two periods.
        """
        absolute_delta = round(current_val - baseline_val, 2)
        if not baseline_val or baseline_val == 0:
            pct_change = 0.0 if absolute_delta == 0 else (100.0 if absolute_delta > 0 else -100.0)
        else:
            pct_change = round((absolute_delta / abs(baseline_val)) * 100.0, 2)
        
        return {
            "current_value": current_val,
            "baseline_value": baseline_val,
            "absolute_delta": absolute_delta,
            "percent_change": pct_change,
            "trend": "increased" if absolute_delta > 0 else ("decreased" if absolute_delta < 0 else "neutral")
        }

    @staticmethod
    def calculate_profitability_metrics(
        gross_revenue: float,
        discounts: float = 0.0,
        cogs: float = 0.0,
        opex_logistics: float = 0.0,
        opex_storage: float = 0.0,
        opex_other: float = 0.0,
        spoilage_loss: float = 0.0
    ) -> Dict[str, Any]:
        """
        Full P&L waterfall calculation with explicit accounting definitions.
        Net Revenue = Gross Revenue - Discounts
        Gross Profit = Net Revenue - COGS
        Gross Margin % = (Gross Profit / Net Revenue) * 100
        Operating OpEx = Logistics + Storage + Other
        Operating Profit (EBITDA) = Gross Profit - Operating OpEx
        Operating Margin % = (Operating Profit / Net Revenue) * 100
        Net Profit = Operating Profit - Spoilage Loss
        Net Margin % = (Net Profit / Net Revenue) * 100
        """
        net_revenue = round(gross_revenue - discounts, 2)
        gross_profit = round(net_revenue - cogs, 2)
        gross_margin_pct = BusinessCalculationEngine.calculate_margin(gross_profit, net_revenue)
        
        total_opex = round(opex_logistics + opex_storage + opex_other, 2)
        operating_profit = round(gross_profit - total_opex, 2)
        operating_margin_pct = BusinessCalculationEngine.calculate_margin(operating_profit, net_revenue)
        
        net_profit = round(operating_profit - spoilage_loss, 2)
        net_margin_pct = BusinessCalculationEngine.calculate_margin(net_profit, net_revenue)

        return {
            "gross_revenue": gross_revenue,
            "discounts": discounts,
            "net_revenue": net_revenue,
            "cogs": cogs,
            "gross_profit": gross_profit,
            "gross_margin_pct": gross_margin_pct,
            "opex_logistics": opex_logistics,
            "opex_storage": opex_storage,
            "opex_other": opex_other,
            "total_opex": total_opex,
            "operating_profit": operating_profit,
            "operating_margin_pct": operating_margin_pct,
            "spoilage_loss": spoilage_loss,
            "net_profit": net_profit,
            "net_margin_pct": net_margin_pct
        }

    @staticmethod
    def calculate_financial_loss_breakdown(
        actual_profit: float,
        baseline_profit: float,
        spoilage_direct_loss: float,
        excess_logistics_cost: float,
        revenue_gap_loss: float = 0.0
    ) -> Dict[str, Any]:
        """
        Reconciles total financial loss against specific identified failure drivers.
        """
        total_gap = round(baseline_profit - actual_profit, 2)
        reconciled_sum = round(spoilage_direct_loss + excess_logistics_cost + revenue_gap_loss, 2)
        unexplained_variance = round(total_gap - reconciled_sum, 2)

        return {
            "total_profit_deficit": total_gap,
            "spoilage_direct_component": spoilage_direct_loss,
            "spoilage_pct_of_loss": BusinessCalculationEngine.calculate_margin(spoilage_direct_loss, total_gap),
            "excess_logistics_component": excess_logistics_cost,
            "logistics_pct_of_loss": BusinessCalculationEngine.calculate_margin(excess_logistics_cost, total_gap),
            "revenue_gap_component": revenue_gap_loss,
            "reconciled_sum": reconciled_sum,
            "unexplained_variance": unexplained_variance,
            "is_fully_reconciled": abs(unexplained_variance) < 1.0
        }

    @staticmethod
    def calculate_logistics_kpis(
        total_shipments: int,
        delayed_shipments: int,
        breached_cold_chain_count: int,
        total_cost_inr: float,
        total_distance_km: float
    ) -> Dict[str, Any]:
        """
        Calculates operational delivery and route KPIs.
        """
        on_time_count = total_shipments - delayed_shipments
        on_time_delivery_rate_pct = BusinessCalculationEngine.calculate_margin(on_time_count, total_shipments)
        cold_chain_breach_rate_pct = BusinessCalculationEngine.calculate_margin(breached_cold_chain_count, total_shipments)
        avg_cost_per_km = round(total_cost_inr / max(total_distance_km, 1.0), 2)
        avg_cost_per_shipment = round(total_cost_inr / max(total_shipments, 1), 2)

        return {
            "total_shipments": total_shipments,
            "delayed_shipments": delayed_shipments,
            "on_time_shipments": on_time_count,
            "on_time_delivery_rate_pct": on_time_delivery_rate_pct,
            "breached_cold_chain_count": breached_cold_chain_count,
            "cold_chain_breach_rate_pct": cold_chain_breach_rate_pct,
            "total_cost_inr": total_cost_inr,
            "total_distance_km": total_distance_km,
            "avg_cost_per_km_inr": avg_cost_per_km,
            "avg_cost_per_shipment_inr": avg_cost_per_shipment
        }

    @staticmethod
    def structure_evidence_and_findings(
        observed_facts: List[str],
        calculated_metrics: Dict[str, Any],
        plausible_explanations: List[str],
        unverified_hypotheses: List[str],
        recommended_actions: List[str]
    ) -> Dict[str, Any]:
        """
        Structures the multi-tier investigation output for explainability and uncertainty handling.
        """
        return {
            "observed_facts": observed_facts,
            "calculated_metrics": calculated_metrics,
            "plausible_explanations": plausible_explanations,
            "unverified_hypotheses": unverified_hypotheses,
            "recommended_actions": recommended_actions,
            "has_uncertainty": len(unverified_hypotheses) > 0
        }

calculation_engine = BusinessCalculationEngine()
