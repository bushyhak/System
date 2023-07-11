function generateHeaders(
	reportTitle = "Report",
	companyName = "Infant Immunization Booking System"
) {
	const doc = new jspdf.jsPDF();
	const pageWidth = doc.internal.pageSize.getWidth();

	// Add Gevac company name at top left corner of report
	doc.setTextColor("#444444");
	doc.setFontSize(12);
	doc.setFont("helvetica", "bold");
	doc.text(companyName, 10, 20);

	// Add report title below company name
	doc.setTextColor("#0074d9");
	doc.setFontSize(20);
	doc.setFont("helvetica", "bold");
	doc.text(reportTitle, pageWidth / 2, 40, { align: "center" });

	// Add date and time of report generation at top right corner of page
	const date = new Date().toLocaleDateString();
	const time = new Date().toLocaleTimeString();
	doc.setFontSize(12);
	doc.setTextColor("#444444");
	doc.setFont("helvetica", "normal");
	doc.text("Report generated on:", pageWidth - 10, 20, { align: "right" });
	doc.text(`${date}, ${time}`, pageWidth - 10, 25, { align: "right" });

	return doc;
}

async function generatePDF(
	title = "Report",
	filename = "report.pdf",
	html = "table"
) {
	const doc = generateHeaders(title);

	const table = document.querySelector(html);
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
				const icon = cell.querySelector("img");
				if (icon) {
					const iconUrl = await imgToDataURL(icon);
					rowData.push({
						content: cell.textContent.trim(),
						image: iconUrl,
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
		headStyles: {
			fillColor: [13, 110, 253],
			textColor: [255, 255, 255],
		},
	});

	doc.save(filename);
}

async function generateTable(
	title = "Report",
	filename = "report.pdf",
	html = "table"
) {
	const doc = generateHeaders(title);
	const images = [];

	doc.autoTable({
		html: html,
		theme: "striped", // 'striped'|'grid'|'plain'
		startX: 10,
		startY: 50,
		headStyles: {
			fillColor: [13, 110, 253],
			textColor: [255, 255, 255],
		},
		didDrawCell: async function (data) {
			if (data.cell.section === "body") {
				const td = data.cell.raw;
				const img = td.querySelector("img");
				if (img) {
					const cell = data.cell;
					const dataURL = await imgToDataURL(img);
					var textPos = data.cell.getTextPos();
					console.log(textPos.x + 15);
					images.push({
						url: dataURL,
						x: textPos.x + 15,
						y: textPos.y,
					});
					console.log(images);
					// data.doc.addImage(
					// 	dataURL,
					// 	"PNG",
					// 	textPos.x + 15,
					// 	textPos.y,
					// 	20,
					// 	20
					// );
				}
			}
		},
	});

	// images.forEach(({ url, x, y }) => {
	// 	doc.addImage(url, "PNG", x, y, 13, 13);
	// });

	// console.log(images[0]);
	// const { url, x, y } = images[0];
	// doc.addImage(url, "PNG", x, y, 15, 15);

	doc.save(filename);
}

function imgToDataURL(img) {
	return new Promise((resolve, reject) => {
		const canvas = document.createElement("canvas");
		const ctx = canvas.getContext("2d");
		const image = new Image();
		image.crossOrigin = "anonymous";
		image.onload = function () {
			canvas.width = this.naturalWidth;
			canvas.height = this.naturalHeight;
			ctx.drawImage(this, 0, 0);
			const dataURL = canvas.toDataURL("image/png");
			resolve(dataURL);
		};
		image.onerror = function () {
			reject(new Error("Failed to load image"));
		};
		image.src = img.src;
	});
}
