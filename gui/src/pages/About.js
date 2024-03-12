import React from "react";
import { LargeTitle } from "../components/sidebar/styles";
import { TextContainer, HorizontalList, StyledLink } from "../components/layout/styles";

const About = () => {
    return (
        <TextContainer>
            <LargeTitle>About</LargeTitle><br />
            GRD-TRT-BUF-4I is the urban transit bus idling detection system drawn 
            from the paper “Global Geolocated Realtime Data of Interfleet Urban 
            Transit Bus Idling”. It offers a global perspective on the emergent 
            behavior of interfleet idling patterns that contribute to worldwide 
            ecological stress, economic inefficiency, and human health risks. 
            This research aims to reduce idling emissions and improve urban air 
            quality by providing a detailed and dynamic picture of interfleet 
            idling behavior around the world to make our global communities 
            healthier and more sustainable while reducing cost and increasing 
            efficiency.<br /><br />

            <h4>Links</h4>
            <HorizontalList>
                <li>
                    Repo: <StyledLink href="https://www.github.com/nickkunz/idling">Github</StyledLink>
                </li>
                <li>
                    Preprint: <StyledLink href="https://arxiv.org/abs/2403.03489.pdf">arXiv</StyledLink>
                </li>
                <li>
                    Test Data: <StyledLink href="https://doi.org/10.6084/m9.figshare.25224224">figshare</StyledLink>
                </li>
            </HorizontalList><br/>

            <HorizontalList>
                <li>
                    <h4>Contacts</h4>
                    Nick Kunz<br/>
                    Cornell University<br/>
                    <StyledLink href="mailto:nhk37@cornell.edu">nhk37@cornell.edu</StyledLink><br/><br/>
                </li>
                <li>
                    <h4>&nbsp;</h4>
                    H. Oliver Gao<br/>
                    Cornell University<br/>
                    <StyledLink href="mailto:hg55@cornell.edu">hg55@cornell.edu</StyledLink><br/><br/>
                </li>
            </HorizontalList>

            <h4>References</h4>
                Kunz, N., Gao, H. O. (2024). Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling. Preprint. <i>arXiv:5451982</i>. <StyledLink href="https://arxiv.org/abs/2403.03489.pdf">https://arxiv.org/abs/2403.03489</StyledLink>.
        </TextContainer>
    );
};

export default About;