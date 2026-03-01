const PermissionModule = {
    // Khởi tạo Select2 cho chọn bộ phận
    initSelect: function(selector) {
        $(selector).select2({
            theme: 'bootstrap-5',
            placeholder: t('placeholder_select_depts'),
            allowClear: true,
            width: '100%'
        });
    },

    // Load quyền của 1 nhân viên lên Select2
    loadRightsToModal: async function(empId, selector) {
        try {
            const res = await fetch(`/api/permissions/view-rights/${empId}`);
            const deptIds = await res.json();
            $(selector).val(deptIds).trigger('change');
        } catch (e) {
            console.error("Lỗi tải quyền xem:", e);
        }
    },

    // Lưu quyền
    saveRights: async function(empId, deptIds) {
        const res = await fetch('/api/permissions/view-rights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_id: empId, dept_ids: dept_ids })
        });
        return await res.json();
    }
};