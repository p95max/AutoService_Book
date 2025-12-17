(() => {
  const ENABLE_SNOW = true; // 🔴 snow on/off
  if (!ENABLE_SNOW) return;

  const canvas = document.getElementById("snow-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d", { alpha: true });
  if (!ctx) return;

  let width = 0;
  let height = 0;
  let snowflakes = [];

  const getTheme = () =>
    document.documentElement.getAttribute("data-theme") || "light";

  const clamp = (v, min, max) => Math.max(min, Math.min(max, v));

  function pickFlakeCount() {
    const base = Math.floor(width / 8);
    const themeFactor = getTheme() === "light" ? 0.85 : 1.0;
    return clamp(Math.floor(base * themeFactor), 70, 180);
  }

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;

    const target = pickFlakeCount();
    if (snowflakes.length < target) {
      for (let i = snowflakes.length; i < target; i++) snowflakes.push(createSnowflake(true));
    } else if (snowflakes.length > target) {
      snowflakes.length = target;
    }
  }

  function createSnowflake(randomY = false) {
    const theme = getTheme();

    const r =
      theme === "light"
        ? Math.random() * 2.6 + 0.7
        : Math.random() * 2.8 + 0.6;

    const opacity =
      theme === "light"
        ? Math.random() * 0.45 + 0.35  // заметнее на белом
        : Math.random() * 0.55 + 0.25;

    return {
      x: Math.random() * width,
      y: randomY ? Math.random() * height : -10 - Math.random() * 60,
      r,
      speed: Math.random() * 1.1 + 0.35,
      drift: Math.random() * 0.7 - 0.35,
      opacity,
    };
  }

  function rebuildFlakes() {
    const count = pickFlakeCount();
    snowflakes = Array.from({ length: count }, () => createSnowflake(true));
  }

  window.addEventListener("resize", resize);

  resize();
  rebuildFlakes();

  function draw() {
    ctx.clearRect(0, 0, width, height);

    const theme = getTheme();

    if (theme === "light") {
      ctx.shadowColor = "rgba(0,0,0,0.18)";
      ctx.shadowBlur = 3;
    } else {
      ctx.shadowColor = "transparent";
      ctx.shadowBlur = 0;
    }

    for (const f of snowflakes) {
      f.y += f.speed;
      f.x += f.drift;

      if (f.x < -30) f.x = width + 30;
      if (f.x > width + 30) f.x = -30;

      if (f.y > height + 15) {
        f.y = -15 - Math.random() * 70;
        f.x = Math.random() * width;
      }

      ctx.beginPath();
      ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);

      if (theme === "dark") {

        ctx.fillStyle = `rgba(255,255,255,${f.opacity})`;
        ctx.fill();
      } else {

        const fillOpacity = Math.min(1, f.opacity);
        ctx.fillStyle = `rgba(130,140,155,${fillOpacity})`;
        ctx.fill();

        ctx.lineWidth = 0.7;
        ctx.strokeStyle = `rgba(90,100,115,${fillOpacity * 0.45})`;
        ctx.stroke();
      }
    }

    requestAnimationFrame(draw);
  }

  draw();

  const mo = new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.type === "attributes" && m.attributeName === "data-theme") {
        rebuildFlakes();
        resize();
        break;
      }
    }
  });
  mo.observe(document.documentElement, { attributes: true });
})();
