from pathlib import Path

# Fix the deeply misplaced indentation and tab scoping in Driverapp.py
path = Path("Driverapp.py")
text = path.read_text(encoding="utf-8", errors="replace")

# Find and replace the problematic second tab1 block with proper indentation
# The second tab1 block (line 64) contains all the earnings form content
# It should remain under tab1 but we need to find where it truly ends

# Find both tab1 occurrences
first_tab1 = text.find("with tab1:\n    st.subheader(\"💰 Earnings Tracker\")")
second_tab1_start = text.find("with tab1:", first_tab1 + 10)  # Find the next tab1

if first_tab1 != -1 and second_tab1_start != -1:
    # Between these two tab1 blocks, we have the placeholder section
    # Replace the first "with tab1:" placeholder to just be a comment or skip it
    # Actually, we'll keep the structure but fix the massive indentation issue
    
    # Find where the tab1 earnings form content ends (should end before "with tab4:")
    tab4_position = text.find("with tab4:", second_tab1_start)
    
    if tab4_position != -1:
        # Extract the content between second tab1 and tab4
        earnings_content_start = text.find("\n", second_tab1_start) + 1
        earnings_section = text[earnings_content_start:tab4_position]
        
        # Fix indentation: remove extra leading spaces
        lines = earnings_section.split('\n')
        fixed_lines = []
        for line in lines:
            # Count leading spaces and reduce indentation
            stripped = line.lstrip()
            if stripped:
                # All content under tab1 should have 4 spaces (one level)
                fixed_lines.append("    " + stripped)
            else:
                fixed_lines.append("")
        
        fixed_earnings = '\n'.join(fixed_lines)
        
        # Reconstruct the file
        new_text = text[:second_tab1_start] + "with tab1:\n" + fixed_earnings + "\n" + text[tab4_position:]
        
        path.write_text(new_text, encoding="utf-8")
        print("Fixed earnings tab indentation and content scoping.")
    else:
        print("Could not find tab4 marker.")
else:
    print("Could not find tab markers.")