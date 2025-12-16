import streamlit as st

# App configuration
st.set_page_config(
    page_title="Package Cost Calculator",
    page_icon="📦",
    layout="wide"
)

# Fixed costs per box type (in dollars)
COSTS = {
    "Small Box": 5.00,
    "Medium Box": 10.00,
    "Large Box": 20.00
}

def calculate_total_cost(total_packages, box_counts):
    """Calculate total cost based on package distribution"""
    total = 0
    breakdown = []
    
    for box_type, count in box_counts.items():
        if count > 0:
            box_cost = count * COSTS[box_type]
            total += box_cost
            breakdown.append(f"{count} {box_type}(s): ${box_cost:.2f}")
    
    return total, breakdown

def main():
    # App title and description
    st.title("📦 Package Cost Calculator")
    st.markdown("""
    Calculate shipping costs based on package quantities and box sizes.
    Enter the total number of packages and select their distribution by box type.
    """)
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Input Parameters")
        
        # Total packages input
        total_packages = st.number_input(
            "**Total Packages Dispatched**",
            min_value=0,
            max_value=1000,
            value=0,
            step=1,
            help="Enter the total number of packages"
        )
        
        st.markdown("---")
        st.subheader("Box Type Distribution")
        
        # Initialize box counts in session state if not exists
        if 'box_counts' not in st.session_state:
            st.session_state.box_counts = {box_type: 0 for box_type in COSTS.keys()}
        
        # Box type distribution inputs
        remaining_packages = total_packages
        box_counts = {}
        
        for i, (box_type, unit_cost) in enumerate(COSTS.items()):
            if i < len(COSTS) - 1:
                max_value = remaining_packages
                help_text = f"Max: {remaining_packages} (${unit_cost:.2f} each)"
            else:
                max_value = remaining_packages
                help_text = f"Auto-filled with remaining packages (${unit_cost:.2f} each)"
            
            count = st.number_input(
                f"**{box_type}**",
                min_value=0,
                max_value=max_value,
                value=min(st.session_state.box_counts.get(box_type, 0), max_value),
                step=1,
                help=help_text,
                key=f"input_{box_type}"
            )
            
            box_counts[box_type] = count
            remaining_packages -= count
        
        # Update session state
        st.session_state.box_counts = box_counts
        
        # Validation check
        if remaining_packages < 0:
            st.error("Total box count exceeds total packages! Please adjust.")
        
        # Reset button
        if st.button("🔄 Reset All", type="secondary"):
            for key in st.session_state.keys():
                if key.startswith('input_'):
                    st.session_state[key] = 0
            st.rerun()
    
    with col2:
        st.header("Cost Calculation")
        
        # Calculate costs
        if total_packages > 0:
            total_cost, breakdown = calculate_total_cost(total_packages, box_counts)
            
            # Display summary
            st.info(f"### Summary")
            st.write(f"**Total Packages:** {total_packages}")
            st.write(f"**Box Types Used:** {sum(1 for count in box_counts.values() if count > 0)}")
            
            st.success(f"### Total Cost: ${total_cost:.2f}")
            
            # Display breakdown
            if breakdown:
                st.markdown("#### 📝 Cost Breakdown:")
                for item in breakdown:
                    st.write(f"- {item}")
            
            # Display cost per package
            if total_packages > 0:
                avg_cost = total_cost / total_packages
                st.metric(
                    label="Average Cost per Package",
                    value=f"${avg_cost:.2f}"
                )
            
            # Data table for visualization
            st.markdown("#### 📈 Distribution Table")
            import pandas as pd
            data = []
            for box_type, count in box_counts.items():
                if count > 0:
                    data.append({
                        "Box Type": box_type,
                        "Quantity": count,
                        "Unit Cost": f"${COSTS[box_type]:.2f}",
                        "Subtotal": f"${count * COSTS[box_type]:.2f}"
                    })
            
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
        else:
            st.warning(Enter package count and select box types to see cost calculation")
    
    # Footer
    st.markdown("---")
    st.caption("**Fixed Costs:** Small Box = $5.00 | Medium Box = $10.00 | Large Box = $20.00")

if __name__ == "__main__":
    main()
