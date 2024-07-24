<div class="flex w-full h-full flex-grow">
  <div class="grid w-80 flex-none card bg-base-300 rounded-box">
    <div class="d-flex justify-content-center gap-1 mb-2 ">
      <button class="btn btn-light"><a class="home-button-anchor-style" href="/home">Home</a></button>
      <button class="btn btn-light"><a href="../dashboard">Dashboard</a></button>
      <button class="btn btn-light"><a href="../phDashboard">Ph.Dashboard</a></button>
      <select class="form-select" id="summary" on:change={moveTo}>
          <option selected disabled>Summary</option>
          <option value="summaryNew">Summary New</option>
          <option value="summaryTotal">Summary Total</option>
          <option value="summaryBetweenDates">Summary Between dates</option>
          <option value="summaryOfISDContacts">Summary of ISD Contacts</option>
          <option value="summaryOfNewContacts">Summary of New Contacts</option>
          <option value="summaryOfWithinDatesContacts">Summary of Within Dates Contacts</option>
          <option value="summaryWithinaState">Summary Within a State</option>
          <option value="summaryOtherThanaState">Summary Other Than a State</option>
          <option value="summaryStateWise">Summary State Wise</option>
          <option value="summaryOnKeyWord">Summary on Key Word</option>
          <option value="multipleNumbersSummary">Multiple Numbers Summary</option>
      </select>
      <select class="form-select" id="callDetails" on:change={moveTo}>
          <option selected disabled>Call Details</option>
          <option value="cdr">CDR</option>
          <option value="gprs">GPRS</option>
          <option value="ipdr">IPDR</option>
          <option value="cdrGprsIpdr">CDR-GPRS-IPDR</option>
          <option value="cdrBetweenDates">CDR Between Dates</option>
          <option value="multiplePhoneNumberCDRS">Multiple Phone Number CDRS</option>
          <option value="cdrBetweenMultiplePhoneNumbers">CDR Between Multiple Phone Numbers</option>
          <option value="imeiCDR">IMEI CDR</option>
          <option value="silentPeriod">Silent Period</option>
          <!-- <option value="commonContacts">Common Contacts</option> -->
          <option value="loopCalls">Loop Calls</option>
      </select>
      <select class="form-select" id="suspectedDB" on:change={moveTo}>
          <option selected disabled>Suspected DB</option>
          <option value="directContacts">Direct Contacts</option>
          <option value="secondLevelContacts">Second Level Contacts</option>
      </select>
      <select class="form-select" id="imeiSearch" on:change={moveTo}>
          <option selected disabled>IMEI Search</option>
          <option value="phonesUsedInImei">Phones Used In IMEI</option>
          <option value="imeisUsedInPhone">IMEIs Used In Phone</option>
          <option value="imeiSearchinfo">IMEI Search Info</option>
      </select>
      <select class="form-select" id="search" on:change={moveTo}>
          <option selected disabled>Search</option>
          <option value="phoneToIMSI">Phone to IMSI</option>
          <option value="imsiSearch">IMSI Search</option>
          <option value="singleAddress">Single Address</option>
          <option value="bulkAddresses">Bulk Addresses</option>
          <option value="cellIdSearch">Cell ID Search</option>
          <option value="cafSearch">CAF Search</option>
          <option value="handsetSearchWithIMEI">Handset Search with IMEI</option>
          <option value="imeiDualAnticipation">IMEI Dual Anticipation</option>
          <option value="otherStateSDRSearch">Other State SDR Search</option>
          <option value="geoBasedSearch">Geo Based Search</option>
          <option value="nickNameSearch">Nickname Search</option>
          <option value="rhSearchByNumber">RH Search by Number</option>
          <option value="poaSearch">POA Search</option>
          <option value="addressSearch">Address Search</option>
          <option value="cellIdDetails">Cell ID Details</option>
          <option value="mobileHandsetAnalysis">Mobile Handset Analysis</option>
          <option value="go614">G.O 614</option>
      </select>
      <select class="form-select" id="locations" on:change={moveTo}>
          <option selected disabled>Locations</option>
          <option value="top10DaysLocations">Top 10 Days Locations</option>
          <option value="top10NightsLocations">Top 10 Nights Locations</option>
          <option value="top10DaysLocationsBetweenDates">Top 10 Days Locations Between Dates</option>
          <option value="top10NightsLocationsBetweenDates">Top 10 Nights Locations Between Dates</option>
          <option value="totalLocations">Total Locations</option>
          <option value="dayAndNightLocations">Day And Night Locations</option>
          <option value="suspectPhonesAtGivenLoc">Suspect Phones at Given Loc</option>
          <option value="suspectPhonesAtMultipleLoc">Suspect Phones at Multiple Loc</option>
          <option value="specificPhonesAtGivenLoc">Specific Phones at Given Loc</option>
      </select>
      <button class="btn btn-light"><a href="/tower_analysis">Tower Analysis</a></button>
      <!-- <select class="form-select" id="analysis" on:change={moveTo}>
          <option selected disabled>Analysis</option>
          <option value="relations">Relations</option>
          <option value="towerCDRAnalysis">Tower CDR Analysis</option>
          <option value="towerGPRSAnalysis">Tower GPRS Analysis</option>
          <option value="towerIPDRAnalysis">Tower IPDR Analysis</option>
      </select> -->

  </div>
  </div>
  <!-- <div class="divider divider-horizontal">OR</div> -->
  <div class="grid h-20 flex-grow card bg-base-300 rounded-box place-items-center">
    <slot />
  </div>
</div>