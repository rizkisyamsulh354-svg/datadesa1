// Admin JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Store original button text for loading state
    document.querySelectorAll('button[type="submit"]').forEach(function(btn) {
        btn.dataset.originalText = btn.innerHTML;
    });
});

// Format Rupiah
function formatRupiah(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

// Confirm delete
function confirmDelete(event) {
    if (!confirm('Yakin ingin menghapus data ini?')) {
        event.preventDefault();
    }
}

// Auto-save form
function autoSaveForm(formId, interval = 30000) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    setInterval(function() {
        // Get form data
        const formData = new FormData(form);
        
        // Save to localStorage
        const data = Object.fromEntries(formData);
        localStorage.setItem('formData_' + formId, JSON.stringify(data));
    }, interval);
}

// Restore form from localStorage
function restoreForm(formId) {
    const saved = localStorage.getItem('formData_' + formId);
    if (saved) {
        const data = JSON.parse(saved);
        Object.keys(data).forEach(key => {
            const field = document.querySelector('[name="' + key + '"]');
            if (field) {
                field.value = data[key];
            }
        });
    }
}

// File size validation
function validateFileSize(input, maxSizeMB = 50) {
    const file = input.files[0];
    if (file) {
        const maxSize = maxSizeMB * 1024 * 1024;
        if (file.size > maxSize) {
            alert('File terlalu besar. Maksimal ' + maxSizeMB + 'MB');
            input.value = '';
            return false;
        }
    }
    return true;
}

// Generate slug from title
function generateSlug(text) {
    return text
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-');
}

// Preview image before upload
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Export data to CSV
function exportDataToCSV(tableId, filename) {
    let csv = [];
    let rows = document.querySelectorAll('#' + tableId + " tr");
    
    for (let i = 0; i < rows.length; i++) {
        let row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (let j = 0; j < cols.length; j++) {
            row.push('"' + cols[j].innerText.replace(/"/g, '""') + '"');
        }
        
        csv.push(row.join(","));
    }
    
    const csvContent = "data:text/csv;charset=utf-8," + encodeURIComponent(csv.join("\n"));
    const link = document.createElement("a");
    link.setAttribute("href", csvContent);
    link.setAttribute("download", filename || "data.csv");
    link.click();
}

// Print table
function printTable(tableId) {
    const printWindow = window.open('', '', 'height=600,width=800');
    const table = document.getElementById(tableId);
    if (table) {
        printWindow.document.write('<html><head><title>Cetak Data</title>');
        printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">');
        printWindow.document.write('</head><body>');
        printWindow.document.write(table.outerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }
}

// Chart helper
function createChart(canvasId, chartType, labels, datasets) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Assuming Chart.js is loaded
    if (typeof Chart !== 'undefined') {
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true
                    }
                }
            }
        });
    }
}
