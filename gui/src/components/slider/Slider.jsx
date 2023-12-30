import React, { useEffect, useState, useRef } from 'react';
import { styled, withStyles } from '@material-ui/core/styles';
import Slider from '@material-ui/core/Slider';
import Button from '@material-ui/core/IconButton';
import PlayIcon from '@material-ui/icons/PlayArrow';
import PauseIcon from '@material-ui/icons/Pause';

const PositionContainer = styled('div')({
    position: 'absolute',
    zIndex: 1,
    bottom: '10px',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
});

const SliderInput = withStyles({
    root: {
        marginLeft: 0,
        width: '25%',
        color: '#808080',
    },
    valueLabel: {
        left: '-70px',
        '& span': {
            background: 'none',
            color: '#000',
            width: '200px'
        }
    }
})(Slider);

export default function RangeInput({ min, max, value: propValue, onChange, isPlaying, setIsPlaying }) {
    const intervalRef = useRef();
    const valueRef = useRef(propValue);
    const [value, setValue] = useState(propValue);
    
    useEffect(() => {
        setValue(propValue);
        valueRef.current = propValue;
    }, [propValue]);

    useEffect(() => {
        if (isPlaying) {
            intervalRef.current = setInterval(() => {
                let newValue = valueRef.current + 1000;
                if (newValue > max) {
                    newValue = min;  // reset to start
                }
                setValue(newValue);
                valueRef.current = newValue;
                onChange(newValue);
            }, 1000);  // update every sec
        } else {
            clearInterval(intervalRef.current);
        }

        return () => clearInterval(intervalRef.current);
    }, [isPlaying, min, max, onChange]);

    return (
        <PositionContainer>
            <Button color="primary" style={{ color: '#808080' }} onClick={() => setIsPlaying(!isPlaying)}>
                {isPlaying ? <PauseIcon title="Stop" /> : <PlayIcon title="Animate" />}
            </Button>
            <SliderInput
                min={min}
                max={max}
                value={value}
                onChange={(event, newValue) => onChange(newValue)}
                valueLabelDisplay="auto"
                valueLabelFormat={value => new Date(value * 1000).toLocaleString() + " (UTC)" }
            />
        </PositionContainer>
    );
}
