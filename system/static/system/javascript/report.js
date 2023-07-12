const favicon = {
	one: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAytJREFUWEfVV11IU2EYfr5z9uPcD/OvLPwLCtTCEWTdRKWkN4UYXYUVBVKQBd0E/VhEhlddSFA3LoN2E4SgoUlF1pXmRUKkq7RMU5xYurl029l2zolzdPMsOzvbMlfv3djL8zzn/Z73/d6P4DpP5ee4LhPwZwBswNqEgwd3d2wio5HkW7/XE1ANa8MbycKDu0oKrDMOgGQnQwAABymwzvJJIhdp/18BeUYKWzNoZOsppKgIfEEejgUOgzMsxn9wMRc1rgpoaeBIoRY1hVpsNtOyJENOFjY7g4dDDIIKWmIWYMmi0bRPjwKTPPGvij7MsqjrnsfInLyKmATs3qhCc4VBLLU0pj0chl0sPAEeBjXBljQamToqIsc+w+JAm1u2WooChLPuqDbBqFkm750M4NYbH/qngxHAQsb2dTTqLDqU56nF/2qfzePFeCBxAS2VBpTlLoIJ0TLgw80+L5R6V6iaXkPwdFSeXLENi9NpdB4yhcl7JgM42jWvSB5zCyjNgYulOpwuSQnjVT924+03Nh58xdyoHmirMsKSpRJBvro57H00pwgYb0JUAe+OmWFYMl/HiB/nXi7Ei6+YLytARQHDJ9PCAPcHGdx47ZEFVFMAiezScK4/yqnJChAAhyQCBPc39HllBTw/bJKdjhabC27/7/sm+hEcN4sDRoj2z36cfyV/BH9FQHuVESVLJvzkYlHRKj/RLuzQ4eCmxXmhoYl4SYUi4QpcKtXhlKQNK1vd4uhVCuHeaKtanh8JCyhKp/FEMog6v/hxtlu5E1ZNgPCl9yr0KM/ThD/6Wo8HtvdM1CKsqoBcI4VOyWUkePmBnUFTvxcuZqWzhfY9UazFlV2pf+6BEMKeHBWa9xtEc4WCYXn0Tgbx0cnCE+ShVxNxV9iZTcOsjbySE/aAtM6l61W4XaaPcLeSGTkesNkX5wcrc30q7gNSEmEm1G7ToqZIu2LxkObN+3l0jfphHWAgrGfRIi4BISDhJEoyaRRnqJCVSiD89gWBaS+HYScrLqaBGPfShAQolT6e//8FAcl8mvFTJN/qrCfgk/c4lTzP6wCs1SN1ige5MzZhbvwJeipiwlaX/4UAAAAASUVORK5CYII=",
	two: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAA3NJREFUWEfFl2tIk2EUx//vtqZT8U5N07wVXotSu0u0LEUKjFzaoKA0L2hZFgSJRSn5yS5KKZIV9cEsJDM080NGpJKmkTcMNaTZvGWm09x06huP6ErdO7c55vP1Pef5/95znnPO81DXAJY3hMkAFU8DdjDAooAegM5uQWE69QzCFApUmgF0F0nQoK9Qz3G0BwB/JQBIJAgAvRLic5o6AxjbWcFysxN49tZgmxphemIS4/3DkLb8wEgbSbFm/6UVAMfUCC7RgXA+JYDlJifGwMm6f0OcX4n2O6WQSQbVBlhjAPtQf/jmRINnZ6VxxibHxtGc/BTtWa8BhoBoBOBx+TA23hABFKWx+P+GbbdL0XDhsUrfJQFcY/bDLzdmnrNCOobOvApIij9B2twFxYgMHB4Xpm5rsFrgA5eofTD3clD6VB/JgKSoVnsAs/V8BDVmgM3jKp373jah9ngW5L3DjNGgWBRcYw/A/VIo+sq/oD7uPrOtujLcUXAejhG7lM4DlV/xfn8apscVOqVClRNjCkiZHRJng+KwZ/xImb3xSsKfb316EycbMQIszL24oAo1oky9iqsF2PooHs4n9yoFP4oy0VVQZTgAwYdU2AZ4KAXLvZIgbZUYDiC45da8Uiq2jcLErxFGABaXA4rNYvw+JZvQrgwXAdhEYmJwlFFg25MzcDqxR+V30ppL1sZqByCoTIXt7n8pKHM/h1EyZBiW3gEWHsLqsJuQvKhhBPBMCYNPWoT+IuAaEwi/3H9h63z4DnVROWoPIc/eCpg9B/65MeCHbJmx1ykFxnxLHOzKAWu2EZHJVuZ2FvLeIY0qYWfhRTiEbdcdgHhuz0/EOlGAUpAMFJIKTS4begEwc+MjqGn+MCJT8HNC3kxrVrf0AkAEVI1jaesPtKYXoftVHSalMiUHmYIWm5zgGL4TbvHBWGVhsrwUzO3sdVUI7+vhi36YnprGmHgAk6NysI1XwXitNTgmRovsyLWsxCFOuz6w0Nrx2C743j0Nro2ZRodwzmio4TvqY3MxWNOxPADizbU2w4bEEDhHCmDiaMvcduUK9Fc0o/NBBbpf1oKeZr4hL3klU40NmHs6zOSbXFJZRhxMyRUY/ynFaEcPhhvFYOr9C/fTDUCrJKg3XtGnGYDelX+ckue5J4TJFKgEAz5Se2nQ91pRmP4XHkhwvq7yEXgAAAAASUVORK5CYII=",
};

function generateHeaders(
	reportTitle = "Report",
	systemName = "Infant Immunization Booking System",
	logo = favicon.one
) {
	const doc = new jspdf.jsPDF();
	const pageWidth = doc.internal.pageSize.getWidth();

	// Add logo to the top left of the report
	doc.addImage(logo, "PNG", 10, 10, scale(32), scale(32));

	// Add Gevac company name at top left corner of report
	doc.setTextColor("#444444");
	doc.setFontSize(12);
	doc.setFont("helvetica", "bold");
	doc.text("Gevac", 12 + scale(32), 7 + scale(32));

	doc.text(systemName, 10, 25);

	// Add report title below company name
	doc.setTextColor("#0074d9");
	doc.setFontSize(20);
	doc.setFont("helvetica", "bold");
	doc.text(reportTitle, pageWidth / 2, 40, { align: "center" });

	// Add date and time of report generation at top right corner of page
	const date_time = moment();
	const date = date_time.format("dddd DD-MMMM-YYYY");
	const time = date_time.format("hh:mm A");
	doc.setFontSize(12);
	// doc.setTextColor("#444444");
	doc.setTextColor(128);
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

function generateTable(
	title = "Report",
	filename = "report.pdf",
	html = "table"
) {
	const doc = generateHeaders(title);

	doc.autoTable({
		html: html,
		theme: "striped", // 'striped'|'grid'|'plain'
		startX: 10,
		startY: 50,
		headStyles: {
			fillColor: [13, 110, 253],
			textColor: [255, 255, 255],
		},
		didDrawCell: function (data) {
			const cell = data.cell;
			if (cell.section === "body") {
				const td = cell.raw;
				const img = td.querySelector("img"); // cell.raw => td element
				if (img) {
					const dataURL = imgToDataURL(img);
					var textPos = cell.getTextPos();
					const x = textPos.x + 9;
					const y = textPos.y;
					const size = scale(13);
					//////////////////////////////////////////////////
					// const text = td.innerText.trim();
					// const fontWidth = parseInt(getComputedStyle(td.children[0]).width);
					// const imgX = textPos.x + cell.padding("left") + cell.lineWidth + textPos.w + size/2;

					const imgX = textPos.x + cell.minReadableWidth + 1 - size;
					//////////////////////////////////////////////////
					data.doc.addImage(dataURL, "PNG", imgX, y, size, size);
				}
			}
		},
	});

	doc.save(filename);
}

function imgToDataURL(img) {
	const canvas = document.createElement("canvas");
	const ctx = canvas.getContext("2d");
	const image = new Image();
	image.crossOrigin = "anonymous";
	image.onload = function () {
		canvas.width = this.naturalWidth;
		canvas.height = this.naturalHeight;
		ctx.drawImage(this, 0, 0);
	};
	image.src = img.src;
	canvas.width = img.naturalWidth;
	canvas.height = img.naturalHeight;
	ctx.drawImage(img, 0, 0);
	const dataURL = canvas.toDataURL("image/png");
	return dataURL;
}

function scale(pixels) {
	return pixels / 3.201;
}
