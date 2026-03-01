const PermissionModule = {
    table: null,

    // 1. Khởi tạo bảng danh sách nhân viên để gán quyền
    initTable: function () {
        if ($.fn.DataTable.isDataTable('#permTable')) {
            $('#permTable').DataTable().destroy();
        }

        this.table = $('#permTable').DataTable({
            ajax: { url: '/api/employees', dataSrc: '' }, // Lấy danh sách NV
            columns: [
                { data: 'FullName' },
                {
                    data: 'ID',
                    render: (id, type, row) => `<div id="rights-badges-${id}" class="small text-muted">Đang tải...</div>`
                },
                {
                    data: 'ID',
                    render: (id) => `
                        <button class="btn btn-sm btn-outline-primary" onclick="PermissionModule.openModal(${id})">
                            <i class="fa-solid fa-user-shield"></i> Phân quyền xem
                        </button>`
                }
            ],
            // Sau khi vẽ bảng xong, load các Badge quyền xem bộ phận
            drawCallback: function () {
                PermissionModule.loadAllBadges();
            }
        });
    },

    // 2. Mở Modal và load dữ liệu hiện tại
    openModal: async function (empId) {
        $('#permEmpId').val(empId);

        // Khởi tạo Select2 nếu chưa có
        $('#viewDeptsSelect').select2({
            theme: 'bootstrap-5',
            dropdownParent: $('#permModal'),
            width: '100%'
        });

        // Load danh sách phòng ban hiện tại của NV
        const res = await fetch(`/api/permissions/view-rights/${empId}`);
        const selectedIds = await res.json();

        $('#viewDeptsSelect').val(selectedIds).trigger('change');
        $('#permModal').modal('show');
    },

    // 3. Lưu quyền
    save: async function () {
        const empId = $('#permEmpId').val();
        const deptIds = $('#viewDeptsSelect').val(); // Mảng các ID

        const res = await fetch('/api/permissions/view-rights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_id: empId, dept_ids: deptIds })
        });

        const result = await res.json();
        if (result.status === "success") {
            Swal.fire(t('save_success'), '', 'success');
            $('#permModal').modal('hide');
            this.table.ajax.reload(); // Load lại bảng để cập nhật badge
        }
    },

    // 4. Load Badge hiển thị các bộ phận NV được xem (Trực quan)
    loadAllBadges: function () {
        // Logic gọi API lấy hàng loạt hoặc render từ dữ liệu có sẵn
        // (Để đơn giản, bạn có thể bổ sung cột ViewDepts vào API /api/employees)
    }
};