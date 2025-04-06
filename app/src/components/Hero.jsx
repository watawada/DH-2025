function HeroSection() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/login"; // Redirect to backend login
  };

  return (
    <section className="hero text-center hero-padding bg-light py-10">
      <div>
        <h1 className="display-4 fw-bold mb-4">Study Buddy</h1>
        <button className="btn btn-secondary mt-3" onClick={handleLogin}>
          Start Learning
        </button>
      </div>
    </section>
  );
}

export default HeroSection;