async function convertToMp3() {
    const url = document.getElementById("youtube_url").value;
    const status = document.getElementById("status");

    if (!url) {
        status.innerText = "Please enter a YouTube URL.";
        return;
    }

    status.innerText = "Converting...";

    try {
        const response = await fetch("http://localhost:5000/convert", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ youtube_url: url }),
        });

        if (!response.ok) throw new Error("Conversion failed");

        const blob = await response.blob();
        const a = document.createElement("a");
        a.href = window.URL.createObjectURL(blob);
        a.download = "converted.mp3";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        status.innerText = "Download complete!";
    } catch (error) {
        status.innerText = `Error: ${error.message}`;
    }
}

