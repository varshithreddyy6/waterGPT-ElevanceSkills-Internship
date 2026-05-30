export default function Footer({ big = false }) {
  if (big) {
    return (
      <footer className="footer big">
        <div className="footer-logo">waterGPT</div>

        <div className="footer-tagline">
          MULTI-MODAL · MULTILINGUAL · INTELLIGENT
        </div>

        <div className="footer-author">
          Developed by Vinayak Varshith Reddy Vangeti · Elevance Skills Internship
        </div>
      </footer>
    );
  }

  return (
    <footer className="footer">
      waterGPT · Powered by Groq · Llama 3.3 70B
      <br />
      Developed by Varshith Reddy Vangeti · varshithreddyy6@gmail.com
    </footer>
  );
}