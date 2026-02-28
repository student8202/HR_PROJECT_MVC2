// Functions for Employee
function openEmpModal() {
    $('#empId').val(''); $('#empModal').modal('show');
    applyLanguage(); // Đảm bảo các label trong Modal được dịch
}
function saveEmp() {
    $.ajax({
        url: '/api/employees/save', type: 'POST', contentType: 'application/json',
        data: JSON.stringify({ FullName: $('#empName').val(), IdDepartment: $('#empDeptSelect').val() }),
        success: () => { $('#empModal').modal('hide'); empTable.ajax.reload(); Swal.fire('Xong!', '', 'success'); }
    });
}
function delEmp(id) {
    if (confirm('Xóa?')) $.ajax({ url: `/api/employees/delete/${id}`, type: 'DELETE', success: () => empTable.ajax.reload() });
}
function delEmp(row) {
    Swal.fire({
        title: t('confirm_delete'),
        html: t('confirm_delete_emp', { name: row.FullName }),
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#6c757d',
        confirmButtonText: t('btn_yes'),
        cancelButtonText: t('btn_cancel'),
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/api/employees/delete/${row.ID}`,
                type: 'DELETE',
                success: function () {
                    empTable.ajax.reload();
                    Swal.fire('Đã xóa!', `Nhân viên <b>${row.FullName}</b> đã bị xóa.`, 'success');
                },
                error: () => Swal.fire('Lỗi', 'Không thể xóa dữ liệu', 'error')
            });
        }
    });
}
// --- HÀM XỬ LÝ SỬA (EDIT) ---

function editEmp(row) {
    $('#empId').val(row.ID); // Gán ID vào hidden input
    $('#empName').val(row.FullName);
    // Cập nhật Select2
    $('#empDeptSelect').val(row.IdDepartment).trigger('change');
    $('#empModal').modal('show');
}

// --- CẬP NHẬT HÀM SAVE (Để gửi cả ID khi sửa) ---

function saveEmp() {
    const payload = {
        ID: $('#empId').val(), // Nếu có ID là sửa, không có là thêm mới
        FullName: $('#empName').val(),
        IdDepartment: $('#empDeptSelect').val()
    };
    $.ajax({
        url: '/api/employees/save',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(payload),
        success: function () {
            $('#empModal').modal('hide');
            empTable.ajax.reload();
            Swal.fire('Thành công!', 'Dữ liệu đã được cập nhật', 'success');
        }
    });
}
// -----------------------
// --- HÀM TẢI FILE MẪU (TEMPLATE) ---
function downloadEmpTemplate() {
    // Chuyển hướng trực tiếp để trình duyệt tự tải file về
    window.location.href = '/api/employees/template';
}

// --- HÀM XUẤT EXCEL (EXPORT) ---
function exportEmpExcel() {
    Swal.fire({
        title: 'Đang chuẩn bị dữ liệu...',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading(); }
    });
    
    // Tải file về
    window.location.href = '/api/employees/export';
    
    // Đóng loading sau 1 giây
    setTimeout(() => { Swal.close(); }, 1500);
}

// --- HÀM NHẬP EXCEL (IMPORT) ---
function handleImportEmp(input) {
    const file = input.files[0];
    if (!file) return;

    // Kiểm tra định dạng file nhanh ở client
    const ext = file.name.split('.').pop().toLowerCase();
    if (ext !== 'xlsx' && ext !== 'xls') {
        Swal.fire('Lỗi', 'Vui lòng chọn file Excel (.xlsx hoặc .xls)', 'error');
        input.value = '';
        return;
    }

    Swal.fire({
        title: 'Đang xử lý dữ liệu...',
        text: 'Vui lòng chờ trong giây lát',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading(); }
    });

    const formData = new FormData();
    formData.append('file', file);

    $.ajax({
        url: '/api/employees/import',
        type: 'POST',
        data: formData,
        processData: false, // Quan trọng: không xử lý dữ liệu
        contentType: false, // Quan trọng: không set contentType mặc định
        success: function (response) {
            input.value = ''; // Reset input để có thể chọn lại file cũ nếu muốn
            empTable.ajax.reload(); // Load lại DataTables
            Swal.fire('Thành công!', response.message, 'success');
        },
        error: function (xhr) {
            input.value = '';
            const msg = xhr.responseJSON ? xhr.responseJSON.error : 'Lỗi kết nối server';
            Swal.fire('Thất bại', msg, 'error');
        }
    });
}