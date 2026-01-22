"""
Script to seed the RAG pipeline with industrial documentation.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.pipeline import get_rag_pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_documents():
    """Seed the vector store with industrial documentation."""
    
    documents = [
        {
            "content": """
            Air Compressor Unit 1 (COMP-001) - Maintenance Manual
            
            Overview:
            The Air Compressor Unit 1 is a rotary screw compressor designed for continuous operation 
            in industrial environments. It provides compressed air at 120-150 PSI for various 
            pneumatic tools and processes.
            
            Normal Operating Parameters:
            - Temperature: 60-80°F (operating), max 90°F
            - Pressure: 120-125 PSI (nominal), 150 PSI (maximum)
            - Vibration: <1.0 mm/s RMS
            - Power Consumption: 45-50 kW
            
            Maintenance Schedule:
            - Daily: Check oil level, inspect for leaks
            - Weekly: Check air filters, drain moisture separator
            - Monthly: Test safety valves, check belt tension
            - Quarterly: Replace air filters, oil analysis
            - Annually: Replace oil, inspect bearings, calibrate sensors
            
            Common Issues:
            1. High Temperature: Usually caused by inadequate ventilation or low oil level
               - Solution: Check oil level, clean cooling fins, verify fan operation
            2. Low Pressure: May indicate air leaks or worn seals
               - Solution: Inspect system for leaks, check valve operation
            3. Excessive Vibration: Often due to misalignment or bearing wear
               - Solution: Check mounting bolts, inspect bearings, verify alignment
            """,
            "metadata": {
                "equipment_id": "COMP-001",
                "doc_type": "manual",
                "category": "maintenance"
            },
            "source": "COMP-001_Manual_v2.3.pdf"
        },
        {
            "content": """
            Gas Turbine 3 (TURB-003) - Operating Procedures
            
            Overview:
            Gas Turbine 3 is a 50MW power generation turbine operating on natural gas. 
            It features advanced blade cooling and requires strict adherence to operating procedures.
            
            Operating Parameters:
            - Operating Temperature: 450-500°F (normal), 550°F (maximum continuous)
            - Exhaust Temperature: 800-900°F
            - Pressure Ratio: 15:1
            - Vibration: <2.0 mm/s RMS
            - Efficiency: 38-42%
            
            Startup Procedure:
            1. Pre-start inspections (30 minutes)
            2. Purge cycle (10 minutes)
            3. Ignition sequence (5 minutes)
            4. Warm-up to operating temperature (20 minutes)
            5. Load ramp-up (gradual over 30 minutes)
            
            Shutdown Procedure:
            1. Reduce load gradually (30 minutes)
            2. Cool-down cycle (45 minutes)
            3. Post-shutdown inspection
            
            Warning Signs:
            - Temperature >520°F: Reduce load immediately, investigate cooling system
            - Vibration >2.5 mm/s: Potential blade imbalance or bearing issue
            - Pressure fluctuations: May indicate fuel system problems
            - Efficiency <35%: Comprehensive inspection required
            
            Emergency Shutdown Triggers:
            - Temperature >550°F
            - Vibration >3.5 mm/s
            - Loss of lubrication
            - Fire detection
            """,
            "metadata": {
                "equipment_id": "TURB-003",
                "doc_type": "procedures",
                "category": "operations"
            },
            "source": "TURB-003_Operations_Manual_v4.1.pdf"
        },
        {
            "content": """
            Hydraulic Pump 7 (PUMP-007) - Troubleshooting Guide
            
            Overview:
            Hydraulic Pump 7 is a variable displacement piston pump serving the hydraulic 
            press system. It operates at high pressure and requires careful monitoring.
            
            Normal Parameters:
            - Operating Pressure: 80-90 bar
            - Temperature: 40-60°C
            - Vibration: <1.5 mm/s RMS
            - Flow Rate: 100-120 L/min
            
            Common Problems and Solutions:
            
            Problem: High Vibration (>3.0 mm/s)
            Possible Causes:
            1. Worn bearings - Symptoms: Metallic noise, heat generation
               Solution: Replace bearing assembly, check alignment
            2. Cavitation - Symptoms: Noise, reduced flow, erratic pressure
               Solution: Check suction line, verify fluid level, inspect filters
            3. Misalignment - Symptoms: Periodic vibration, coupling wear
               Solution: Re-align pump and motor, check mounting
            
            Problem: Temperature Increase (>80°C)
            Possible Causes:
            1. Low fluid level - Check reservoir, add fluid if needed
            2. Contaminated fluid - Perform fluid analysis, replace if contaminated
            3. Internal leakage - Pressure test, inspect seals and pistons
            4. Excessive load - Review system pressure settings, reduce if possible
            
            Problem: Pressure Fluctuations
            Possible Causes:
            1. Air in system - Bleed system, check for suction leaks
            2. Worn pump components - Inspect pistons, valve plate, cylinder block
            3. Contaminated fluid - Replace fluid and filters
            
            Bearing Replacement Procedure:
            1. Drain hydraulic fluid
            2. Disconnect coupling
            3. Remove pump from mounting
            4. Disassemble pump housing
            5. Press out old bearings
            6. Install new bearings with proper preload
            7. Reassemble with new seals
            8. Align and mount pump
            9. Fill with fresh fluid
            10. Test run and verify parameters
            
            Preventive Maintenance:
            - Monthly: Check vibration levels, inspect for leaks
            - Quarterly: Fluid analysis, filter replacement
            - Semi-annually: Bearing inspection, seal check
            - Annually: Complete overhaul if vibration trends upward
            """,
            "metadata": {
                "equipment_id": "PUMP-007",
                "doc_type": "troubleshooting",
                "category": "maintenance"
            },
            "source": "PUMP-007_Troubleshooting_Guide_v3.2.pdf"
        },
        {
            "content": """
            Vibration Analysis Guide - All Rotating Equipment
            
            Understanding Vibration Measurements:
            Vibration is measured in mm/s RMS (root mean square) and indicates the health 
            of rotating equipment. Regular monitoring can predict failures before they occur.
            
            Severity Levels:
            - 0-1.0 mm/s: Excellent condition
            - 1.0-2.0 mm/s: Good condition, acceptable
            - 2.0-3.0 mm/s: Fair condition, monitor closely
            - 3.0-4.5 mm/s: Poor condition, plan maintenance
            - >4.5 mm/s: Critical, immediate action required
            
            Common Vibration Causes:
            
            1. Imbalance
               - Characteristics: Vibration at 1x running speed
               - Causes: Uneven mass distribution, material buildup, component wear
               - Solution: Balance rotor, clean components
            
            2. Misalignment
               - Characteristics: High axial vibration, 2x running speed
               - Causes: Improper installation, thermal growth, foundation settling
               - Solution: Precision alignment, check mounting
            
            3. Bearing Defects
               - Characteristics: High frequency vibration, may be intermittent
               - Causes: Wear, contamination, inadequate lubrication
               - Solution: Replace bearings, improve lubrication
            
            4. Looseness
               - Characteristics: Multiple frequency peaks, directional
               - Causes: Worn bearings, loose mounting bolts, structural issues
               - Solution: Tighten connections, replace worn parts
            
            5. Resonance
               - Characteristics: High amplitude at specific speeds
               - Causes: Natural frequency matches operating frequency
               - Solution: Change operating speed, modify structure, add damping
            
            Monitoring Best Practices:
            - Take readings at same locations and times
            - Monitor trends over time, not just absolute values
            - Compare readings to baseline and OEM specifications
            - Investigate sudden changes (>25% increase)
            - Consider operating conditions (load, temperature)
            """,
            "metadata": {
                "doc_type": "guide",
                "category": "diagnostics"
            },
            "source": "Vibration_Analysis_Guide_General.pdf"
        },
        {
            "content": """
            Predictive Maintenance Program - Equipment Health Monitoring
            
            Introduction:
            Predictive maintenance uses condition monitoring to predict equipment failures 
            before they occur, reducing downtime and maintenance costs.
            
            Key Monitoring Parameters:
            
            1. Vibration Analysis
               - Frequency: Weekly for critical equipment, monthly for others
               - Tools: Vibration sensors, spectrum analyzers
               - Indicators: Trending increases, frequency changes
            
            2. Temperature Monitoring
               - Frequency: Continuous via sensors
               - Tools: IR cameras, thermocouples, RTDs
               - Indicators: Hot spots, gradual temperature rise
            
            3. Oil Analysis
               - Frequency: Quarterly or based on hours
               - Parameters: Viscosity, contamination, wear metals
               - Indicators: Particle count increase, viscosity change
            
            4. Ultrasonic Testing
               - Frequency: Monthly
               - Applications: Leak detection, electrical inspection
               - Indicators: Amplitude changes, frequency shifts
            
            Failure Prediction Models:
            
            Bearing Failure Indicators:
            - Vibration increase >50% from baseline
            - Temperature increase >15°C
            - High frequency noise
            - Typical lead time: 2-8 weeks
            
            Seal Failure Indicators:
            - Gradual pressure loss
            - Visible leakage
            - Temperature changes around seal area
            - Typical lead time: 1-4 weeks
            
            Motor Winding Failure:
            - Insulation resistance decrease
            - Temperature imbalance between phases
            - Current imbalance
            - Typical lead time: 2-12 weeks
            
            Implementation Strategy:
            1. Establish baselines for all equipment
            2. Define monitoring frequencies
            3. Set alarm thresholds (warning and critical)
            4. Create response procedures
            5. Track and analyze failure modes
            6. Continuously refine thresholds
            
            Cost-Benefit Analysis:
            - Reduced unplanned downtime: 30-50%
            - Extended equipment life: 20-40%
            - Lower maintenance costs: 10-30%
            - Improved safety and reliability
            - ROI typically achieved within 6-12 months
            """,
            "metadata": {
                "doc_type": "program",
                "category": "predictive_maintenance"
            },
            "source": "Predictive_Maintenance_Program_Overview.pdf"
        }
    ]
    
    try:
        logger.info("Initializing RAG pipeline...")
        rag = get_rag_pipeline()
        
        logger.info(f"Adding {len(documents)} documents to vector store...")
        rag.add_documents(documents)
        
        logger.info("Document seeding completed successfully!")
        
        # Test search
        logger.info("\nTesting search functionality...")
        test_query = "What causes high vibration in pumps?"
        results = rag.search(test_query, k=2)
        
        logger.info(f"\nTest query: '{test_query}'")
        logger.info(f"Found {len(results)} relevant documents")
        
        for i, result in enumerate(results, 1):
            logger.info(f"\nResult {i}:")
            logger.info(f"Source: {result['source']}")
            logger.info(f"Content preview: {result['content'][:200]}...")
        
    except Exception as e:
        logger.error(f"Error seeding documents: {str(e)}")
        raise


if __name__ == "__main__":
    seed_documents()
