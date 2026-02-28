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
