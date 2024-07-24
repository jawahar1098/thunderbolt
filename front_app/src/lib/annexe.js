// @ts-nocheck
const today = new Date();
const year = today.getFullYear(); // Get the four-digit year
const month = String(today.getMonth() + 1).padStart(2, "0"); // Get the month (0-11) and add leading zero if necessary
const day = String(today.getDate()).padStart(2, "0"); // Get the day of the month and add leading zero if necessary

export async function generatePDF(data, cont, circle) {
    console.log(data, cont, circle, '');
    const content = cont;
    const pdfOptions = {
        margin: [0,0,0,0.3],
        filename: `${data.token}_${circle}.pdf`,
        image: {
            type: "jpeg",
            quality: 0.95
        },
        html2canvas: {
            scale: 1.5
        },
        jsPDF: {
            unit: "cm",
            format: "a4",
            orientation: "portrait"
        },
    };
    await html2pdf().from(content).set(pdfOptions).save();
}

// export async function generatePDFsAndZip(dataList, cont, circle) {
//     const zip = new JSZip();
//     for (const data of dataList) {
//         const pdfBlob = await generatePDF(data, cont, circle);
//         zip.file(`${data.token}_${circle}.pdf`, pdfBlob);
//     }
//     const zipBlob = await zip.generateAsync({ type: "blob" });
//     saveAs(zipBlob, `${year}${month}${day}_${circle}_PDFs.zip`);
// }
