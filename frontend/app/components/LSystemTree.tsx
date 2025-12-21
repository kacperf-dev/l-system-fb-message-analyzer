"use client";
import React, { useRef } from "react";
import dynamic from "next/dynamic";
import p5Types from "p5";

const Sketch = dynamic(() => import("react-p5").then((mod) => mod.default), {
    ssr: false
});

interface LSystemProps {
    word: string;
}

const LSystemTree: React.FC<LSystemProps> = ({ word }) => {
    const instructions = word.match(/\w\([\d.,-]+\)|\[|\]|\+|-/g) ?? [];
    const totalTrunks = (word.match(/T/g) || []).length;
    
    const ANIMATION_DURATION = 5000; 
    
    const animState = useRef({
        startTime: 0,
        isStarted: false
    });

    const setup = (p5: p5Types, canvasParentRef: Element) => {
        p5.createCanvas(p5.windowWidth, p5.windowHeight).parent(canvasParentRef);
        animState.current.startTime = p5.millis();
        animState.current.isStarted = true;
    };

    const easeOutQuad = (t: number): number => {
        return t * (2 - t);
    };

    const draw = (p5: p5Types) => {
        p5.background("#87ceeb");
        drawGround(p5);

        let currentProgress = 0;
        if (animState.current.isStarted) {
            const currentTime = p5.millis();
            const elapsed = currentTime - animState.current.startTime;
            const rawT = p5.constrain(elapsed / ANIMATION_DURATION, 0, 1);
            const easedT = easeOutQuad(rawT);
            currentProgress = easedT * instructions.length;
        } else {
            currentProgress = 0;
        }

        const startX = p5.width / 2;
        const startY = p5.height;

        p5.push();
        p5.translate(startX, startY);
        parseTree(p5, "wood", currentProgress); 
        p5.pop();

        p5.push();
        p5.translate(startX, startY);
        parseTree(p5, "fruit", currentProgress);
        p5.pop();
    };

    const parseTree = (p5: p5Types, drawType: "wood" | "fruit", maxProgress: number) => {
        let trunkCount = 0;
        let currentAngle = 0;
        let fruitIndexCounter = 0; 
        const angleStack: number[] = [];

        p5.noiseSeed(99);

        const activeIndex = Math.floor(maxProgress);
        const activeScale = maxProgress % 1;

        for (let i = 0; i < instructions.length; i++) {
            const cmd = instructions[i];
            const params = cmd.match(/[\d.-]+/g)?.map(Number) ?? [];

            let scaleFactor = 0; 

            if (i < activeIndex) {
                scaleFactor = 1;
            } else if (i === activeIndex) {
                scaleFactor = easeOutQuad(activeScale);
            } 

            if (cmd.startsWith("T")) {
                const fullH = params[0] ?? 20;
                const h = fullH * scaleFactor; 

                if (drawType === "wood" && scaleFactor > 0) {
                    const startW = p5.map(trunkCount, 0, totalTrunks, 26, 6);
                    const endW = p5.map(trunkCount + 1, 0, totalTrunks, 26, 6);

                    p5.noStroke();
                    p5.fill("#3d2b1f");
                    p5.beginShape();
                    p5.vertex(-startW / 2, 0);
                    p5.vertex(startW / 2, 0);
                    p5.vertex(endW / 2, -h);
                    p5.vertex(-endW / 2, -h);
                    p5.endShape(p5.CLOSE);
                }
                
                p5.translate(0, -h);
                trunkCount++; 
            } 
            else if (cmd.startsWith("M")) {
                const fullD = params[0] ?? 50;
                const d = fullD * scaleFactor;
                
                if (drawType === "wood" && scaleFactor > 0) {
                    p5.stroke("#5d4037");
                    p5.strokeWeight(2);
                    p5.line(0, 0, 0, -d);
                }
                p5.translate(0, -d);
            } 
            else if (cmd.startsWith("W")) {
                if (drawType === "wood") {
                    p5.strokeWeight(params[0] ?? 1);
                }
            } 
            else if (cmd.startsWith("F")) {
                const [s, c] = params;
                fruitIndexCounter++;
                
                if (drawType === "fruit" && scaleFactor > 0.01) {
                    drawFruit(p5, s ?? 0.5, c ?? 1, currentAngle, fruitIndexCounter, scaleFactor);
                }
            }
            else if (cmd === "[") {
                p5.push();
                angleStack.push(currentAngle);

                const noiseVal = p5.noise(i * 0.5);
                const fullBareLength = p5.map(noiseVal, 0, 1, 40, 60);
                const bareBranchLength = fullBareLength * scaleFactor;

                if (drawType === "wood" && scaleFactor > 0) {
                    p5.stroke("#5d4037");
                    p5.strokeWeight(2);
                    p5.line(0, 0, 0, -bareBranchLength);
                }

                p5.translate(0, -bareBranchLength);
            }
            else if (cmd === "]") {
                p5.pop();
                const restored = angleStack.pop();
                if (restored !== undefined) currentAngle = restored;
            }
            else if (cmd === "+") {
                 const variance = p5.noise(trunkCount * 0.1) * 20 - 10;
                 const angleChange = p5.radians(35 + variance);
                 p5.rotate(angleChange);
                 currentAngle += angleChange;
            }
            else if (cmd === "-") {
                 const variance = p5.noise(trunkCount * 0.1) * 20 - 10;
                 const angleChange = p5.radians(-35 - variance);
                 p5.rotate(angleChange);
                 currentAngle += angleChange;
            }
        }
    }

    const drawFruit = (p5: p5Types, sentiment: number, count: number, branchAngle: number, fruitIndex: number, growthScale: number) => {
        p5.push();
        p5.rotate(-branchAngle);

        const isEven = fruitIndex % 2 === 0;
        const stableRandom = p5.noise(fruitIndex * 12.34); 
        
        let fullStemLength;
        if (isEven) {
            fullStemLength = 10 + stableRandom * 5;
        } else {
            fullStemLength = 40 + stableRandom * 10;
        }

        const currentStemLength = fullStemLength * growthScale;
        
        p5.stroke("#3e2723"); 
        p5.strokeWeight(0.8); 
        p5.line(0, 0, 0, currentStemLength);

        p5.translate(0, currentStemLength);

        const colorNegative = p5.color("#e57373");
        const colorNeutral = p5.color("#ffd54f");
        const colorPositive = p5.color("#81c784");

        let fruitColor;
        if (sentiment < 0.5) {
            const t = p5.map(sentiment, 0, 0.5, 0, 1);
            fruitColor = p5.lerpColor(colorNegative, colorNeutral, t);
        } else {
            const t = p5.map(sentiment, 0.5, 1, 0, 1);
            fruitColor = p5.lerpColor(colorNeutral, colorPositive, t);
        }

        const fullFruitSize = p5.map(Math.log10(count + 1), 0, 4, 4, 12); 
        const fruitSize = fullFruitSize * growthScale;
        
        p5.noStroke();
        p5.fill(fruitColor);
        
        p5.beginShape();
        p5.vertex(0, 0);
        p5.bezierVertex(fruitSize, fruitSize * 0.5, fruitSize, fruitSize * 1.5, 0, fruitSize * 1.8);
        p5.bezierVertex(-fruitSize, fruitSize * 1.5, -fruitSize, fruitSize * 0.5, 0, 0);
        p5.endShape();
        
        p5.fill(255, 70);
        p5.ellipse(-fruitSize * 0.3, fruitSize * 0.8, fruitSize * 0.4, fruitSize * 0.4);

        p5.pop();
    };

    const drawGround = (p5: p5Types) => {
        const grassColors = ["#1d2e28", "#14452f", "#0f5132", "#2d6a4f", "#40916c"];
        p5.noFill();
        
        for (let i = 0; i < p5.width; i += 3) {
            const colorIndex = Math.floor(p5.noise(i * 0.01) * grassColors.length);
            p5.stroke(grassColors[colorIndex]);
            p5.strokeWeight(2);
            const h = p5.noise(i * 0.02) * 50 + 20;
            const windSpeed = p5.frameCount * 0.02;
            const windWave = i * 0.01;
            const windOffset = p5.sin(windSpeed + windWave) * 15;

            p5.beginShape();
            p5.curveVertex(i, p5.height + 10);
            p5.curveVertex(i, p5.height);
            p5.curveVertex(i + windOffset * 0.5, p5.height - h * 0.7);
            p5.curveVertex(i + windOffset, p5.height - h);
            p5.curveVertex(i + windOffset, p5.height - h);
            p5.endShape();
        }
    };

    const windowResized = (p5: p5Types) => {
        p5.resizeCanvas(p5.windowWidth, p5.windowHeight);
    };

    return <Sketch setup={setup} draw={draw} windowResized={windowResized} />;
};

export default LSystemTree;