"use client";
import React from "react";
import dynamic from "next/dynamic";
import p5Types from "p5";

const Sketch = dynamic(() => import("react-p5").then((mod) => mod.default), {
    ssr: false
});

const LSystemTree: React.FC = () => {
    const setup = (p5: p5Types, canvasParentRef: Element) => {
        p5.createCanvas(window.innerWidth, window.innerHeight).parent(
            canvasParentRef
        );
    }

    const draw = (p5: p5Types) => {
        p5.background("#f0f0dc");
        drawGround(p5, p5.width, p5.height);
    }

    const drawGround = (p5: p5Types, screenWidth: number, screenHeight: number) => {
        const grassColors = ["#1d2e28", "#14452f", "#0f5132"];
        p5.noFill();
        p5.stroke("#3a5a40");
        p5.strokeWeight(1.5);

        for (let i = 0; i < screenWidth; i += 0.6) {
            const colorIndex = Math.floor(p5.noise(i) * grassColors.length);
            p5.stroke(grassColors[colorIndex]);
            const h = p5.noise(i * 0.1) * 40 + 10;
            
            const wind = p5.sin(p5.frameCount * 0.015 + i) * 15;

            p5.beginShape();
            p5.curveVertex(i - wind, screenHeight + 50);
            p5.curveVertex(i, screenHeight);
            p5.curveVertex(i + wind, screenHeight - h);
            p5.curveVertex(i + wind * 2, screenHeight - h - 20);
            p5.endShape();
        }
    }


    return <Sketch setup={setup} draw={draw} />
};

export default LSystemTree;