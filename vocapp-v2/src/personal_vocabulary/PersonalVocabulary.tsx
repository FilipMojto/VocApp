
import '../styles/search_bar.css'
import './styles/personal_vocabulary.css'
import './styles/lexical_entries_section.css'
import './styles/mapped_translations_section.css'

import { useState } from 'react'
import { useEffect } from 'react'
import { useRef } from 'react'
import InputIconContainer from '../components/icon_slots/input_icon_container/InputIconContainer'
import IconContainer from '../components/icon_slots/icon_container/IconContainer'
// import InputIconContainer from './components/icon_slots/input_icon_container/InputIconContainer'
import ButtonIconContainer from '../components/icon_slots/label_icon_container/ButtonIconContainer'


function PersonalVocabulary() {
    return (
        <>
            <div id='personal-vocabulary-window'>
                
                <header id='pvw-header'>
                    <h1>Personal Vocabulary</h1>
                    {/* <hr></hr> */}
                </header>

                <main id='pvw-content-container'>
                    <section id='pvw-lexical-entries-section' className='pvw-card'>
                        <h2 className='section-title'>Entries</h2>

                        <div id="les-table" role="table" aria-label="Lexeme list">
                            <div className="les-table-row" role="row">
                                <div className="les-table-cell" role="columnheader">No.</div>
                                <div className="les-table-cell" role="columnheader">Lexeme</div>
                                <div className="les-table-cell" role="columnheader">Pack</div>
                            </div>

                            <div className="les-table-row" role="row">
                                <div className="les-table-cell" role="cell">1</div>
                                <div className="les-table-cell" role="cell">organizovať akciu</div>
                                <div className="les-table-cell" role="cell">Basic</div>
                            </div>

                            <div className="les-table-row" role="row">
                                <div className="les-table-cell" role="cell">2</div>
                                <div className="les-table-cell" role="cell">zvýšiť povedomie</div>
                                <div className="les-table-cell" role="cell">Basic</div>
                            </div>
                        </div>

                        <div id='les-table-control-panel' className='pvw-card-control-panel'>
                            {/* <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>

                            <input type='text' placeholder='Search...' id='les-search-input'/> */}

                            <InputIconContainer
                                icon={
                                    <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    strokeWidth="1.5"
                                    stroke="currentColor"
                                    className="w-5 h-5"
                                >
                                    <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                                    />
                                </svg>
                                }
                                placeholder="Search entry"
                                // containerClassName="add-entry-input-container"
                                // iconContainerClassName="add-entry-input-icon-container"
                                // inputClassName="add-entry-input"
                                onChange={(e) => console.log("Input changed:", e.target.value)}
                            />

                            <ButtonIconContainer
                                icon={
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-5 h-5">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                    </svg>
                                }
                                label="Add Entry"
                            />
                        </div>
                    </section>

                    <section id="pvw-mapped-translations-section" className="pvw-card table-card">
                        <h2 className="section-title">Mapped Translations</h2>
                        <div className="table-wrapper">
                            <table className="styled-table">
                                <thead>
                                    <tr>
                                    <th>No.</th>
                                    <th>Lexeme</th>
                                    <th>Category</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                    <td data-label="No.">1.</td>
                                    <td data-label="Lexeme">to hold an event</td>
                                    <td data-label="Category">Formal</td>
                                    </tr>
                                    <tr>
                                    <td data-label="No.">2.</td>
                                    <td data-label="Lexeme">to organize an event</td>
                                    <td data-label="Category">Neutral</td>
                                    </tr>
                                    <tr>
                                    <td data-label="No.">3.</td>
                                    <td data-label="Lexeme">to throw a party</td>
                                    <td data-label="Category">Informal</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div id='mts-control-panel' className='pvw-card-control-panel'>
                            <ButtonIconContainer
                                    icon={
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-5 h-5">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                    </svg>
                                }
                                    label="Add Translation">
                            </ButtonIconContainer>
                            <ButtonIconContainer
                                icon={
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m6 4.125 2.25 2.25m0 0 2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                                    </svg>
                                }
                                label="Delete Translation">
                            </ButtonIconContainer>
                        </div>
                    </section>
                </main>
            </div>
        </>
    )
}

export default PersonalVocabulary