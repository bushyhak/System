function generatePDF(title = "Report", filename = "report.pdf") {
	const doc = new jspdf.jsPDF();
	const pageWidth = doc.internal.pageSize.getWidth();

	// Add Gevac company name at top left corner of report
	doc.setTextColor("#444444");
	doc.setFontSize(12);
	doc.setFont("helvetica", "bold");
	doc.text("Infant Immunization Booking System", 10, 20);

	// Add report title below company name
	doc.setTextColor("#0074d9");
	doc.setFontSize(20);
	doc.setFont("helvetica", "bold");
	doc.text(title, pageWidth / 2, 40, { align: "center" });

	// Add date and time of report generation at top right corner of page
	const date = new Date().toLocaleDateString();
	const time = new Date().toLocaleTimeString();
	doc.setFontSize(12);
	doc.setTextColor("#444444");
	doc.setFont("helvetica", "regular");
	doc.text("Report generated on:", pageWidth - 10, 20, { align: "right" });
	doc.text(`${date}, ${time}`, pageWidth - 10, 25, { align: "right" });

	const table = document.querySelector("table");
	const tableData = [];
	const headers = [];
	const rows = table.rows;
	for (let i = 0; i < rows.length; i++) {
		const row = rows[i];
		const rowData = [];
		const cells = row.cells;
		for (let j = 0; j < cells.length; j++) {
			const cell = cells[j];
			if (i === 0) {
				headers.push(cell.textContent);
			} else {
				const icon = cell.querySelector("i");
				if (icon) {
					// const iconUrl = getIconUrl(icon);
					rowData.push({
						content: cell.textContent.trim(),
						// image: iconUrl,
						// styles: { font: "FontAwesome" },
					});
				} else {
					rowData.push(cell.textContent);
				}
			}
		}
		if (i !== 0) {
			tableData.push(rowData);
		}
	}

	// Add table below header information
	doc.autoTable({
		head: [headers],
		body: tableData,
		startY: 50,
		startX: 10,
		headerStyles: {
			fillColor: [13, 110, 253],
			textColor: [255, 255, 255],
		},
	});

	doc.save(filename);
}

// function getIconUrl(icon) {
// 	const canvas = document.createElement("canvas");
// 	canvas.width = icon.offsetWidth;
// 	canvas.height = icon.offsetHeight;
// 	const context = canvas.getContext("2d");
// 	const svgString = new XMLSerializer().serializeToString(icon);
// 	const svg = new Blob([svgString], { type: "image/svg+xml;charset=utf-8" });
// 	const url = URL.createObjectURL(svg);
// 	const img = new Image();
// 	img.onload = function () {
// 		context.drawImage(img, 0, 0);
// 		URL.revokeObjectURL(url);
// 	};
// 	img.src = url;
// 	return canvas.toDataURL("image/png");
// }
