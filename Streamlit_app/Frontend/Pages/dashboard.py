import streamlit as st
import os
from utils.logger import log_dashboard_access
from utils.database import get_all_registrations, get_registration_count



def render_dashboard():
    # Log dashboard access (only once when page loads)
    if st.session_state.user_data:
        # Use session state to track if already logged
        if "dashboard_logged" not in st.session_state:
            log_dashboard_access(
                st.session_state.user_data.get("name", "Unknown"),
                st.session_state.user_data.get("email", "Unknown")
            )
            st.session_state.dashboard_logged = True
    
    st.title("✅ Welcome to Dashboard!")
    
    if st.session_state.user_data:
        st.success("🎉 Registration Successful!")
        
        st.markdown("---")
        
        st.subheader("📋 Your Details:")
        st.write(f"**👤 Name:** {st.session_state.user_data['name']}")
        st.write(f"**📧 Email:** {st.session_state.user_data['email']}")
        st.write(f"**📅 Registered On:** {st.session_state.user_data['registration_date']}")
        
        # Show uploaded file info if exists
        if st.session_state.user_data.get('file_path'):
            file_path = st.session_state.user_data['file_path']
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"📥 Download Your File: {filename}",
                        data=f.read(),
                        file_name=filename,
                        mime="text/plain"
                    )
        
        st.markdown("---")
    
    # BACKUP SECTION - Download All Files to User's Computer
    st.markdown("---")
    st.header("📦 Backup All Uploaded Files")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("💡 Click the button below to download ALL uploaded files as a ZIP archive to your computer")
    
    with col2:
        try:
            registrations = get_all_registrations()
            total_files = sum(1 for reg in registrations if len(reg) > 5 and reg[5] and os.path.exists(reg[5]))
            st.metric("Files Available", total_files)
        except:
            st.metric("Files Available", "N/A")
    
    if st.button("💾 Create Backup & Download", type="primary", use_container_width=True):
        import zipfile
        from datetime import datetime
        import io
        
        try:
            # Get all registrations with file paths
            registrations = get_all_registrations()
            
            # Filter only existing files
            file_paths = []
            for reg in registrations:
                if len(reg) > 5 and reg[5] and os.path.exists(reg[5]):
                    file_paths.append({
                        'path': reg[5],
                        'user_name': reg[1],
                        'email': reg[2]
                    })
            
            if file_paths:
                # Create progress indicator
                with st.spinner('Creating backup... Please wait...'):
                    # Create ZIP file in memory
                    zip_buffer = io.BytesIO()
                    
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file_info in file_paths:
                            file_path = file_info['path']
                            filename = os.path.basename(file_path)
                            
                            # Add file to ZIP with original filename
                            zip_file.write(file_path, filename)
                    
                    # Reset buffer position
                    zip_buffer.seek(0)
                    
                    # Generate timestamp for backup filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_filename = f"backup_all_files_{timestamp}.zip"
                    
                    st.success(f"✅ Backup created successfully! {len(file_paths)} files ready to download.")
                
                # Show download button
                st.download_button(
                    label=f"📥 Download Backup ZIP ({len(file_paths)} files)",
                    data=zip_buffer,
                    file_name=backup_filename,
                    mime="application/zip",
                    type="primary",
                    use_container_width=True
                )
                
                # Show file list
                with st.expander("📋 View Files Included in Backup"):
                    for idx, file_info in enumerate(file_paths, 1):
                        filename = os.path.basename(file_info['path'])
                        st.write(f"{idx}. **{filename}** - Uploaded by: {file_info['user_name']} ({file_info['email']})")
                
            else:
                st.warning("⚠️ No files found to backup. Upload some files first!")
                
        except Exception as e:
            st.error(f"❌ Backup failed: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        # Clear dashboard log flag
        if "dashboard_logged" in st.session_state:
            del st.session_state.dashboard_logged
        
        st.session_state.page = "registration"
        st.session_state.user_data = None
        st.rerun()
    
    # NEW SECTION: Show all registrations from database
    st.markdown("---")
    st.header("📊 All Registrations (Database)")
    
    try:
        total_count = get_registration_count()
        st.metric("Total Registrations in Database", total_count)
        
        registrations = get_all_registrations()
        
        if registrations:
            for reg in registrations:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 2])
                    col1.write(f"**#{reg[0]}**")
                    col2.write(f"**{reg[1]}**")
                    col3.write(f"{reg[2]}")
                    st.caption(f"📅 Registered: {reg[4]}")
                    
                    # Show file download link if file exists (NEW!)
                    if len(reg) > 5 and reg[5]:
                        file_path = reg[5]
                        if os.path.exists(file_path):
                            filename = os.path.basename(file_path)
                            with open(file_path, "rb") as f:
                                st.download_button(
                                    label=f"📥 Download {filename}",
                                    data=f.read(),
                                    file_name=filename,
                                    mime="text/plain",
                                    key=f"download_{reg[0]}"  # Unique key per button
                                )
                        else:
                            st.caption(f"📎 File: {os.path.basename(file_path)} (not found)")
                    
                    st.divider()
        else:
            st.info("📭 No registrations in database yet!")
    except Exception as e:
        st.error(f"❌ Could not load registrations: {e}")
