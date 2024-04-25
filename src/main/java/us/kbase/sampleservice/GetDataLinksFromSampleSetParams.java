
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: GetDataLinksFromSampleSetParams</p>
 * <pre>
 * get_data_links_from_sample_set parameters.
 * sample_ids - a list of sample ids and versions
 * effective_time - the time at which the query was run. This timestamp, if saved, can be
 *     used when running the method again to enqure reproducible results. Note that changes
 *     to workspace permissions may cause results to change over time.
 * as_admin - run the method as a service administrator. The user must have read
 *     administration permissions.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "sample_ids",
    "effective_time",
    "as_admin"
})
public class GetDataLinksFromSampleSetParams {

    @JsonProperty("sample_ids")
    private List<SampleIdentifier> sampleIds;
    @JsonProperty("effective_time")
    private Long effectiveTime;
    @JsonProperty("as_admin")
    private Long asAdmin;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("sample_ids")
    public List<SampleIdentifier> getSampleIds() {
        return sampleIds;
    }

    @JsonProperty("sample_ids")
    public void setSampleIds(List<SampleIdentifier> sampleIds) {
        this.sampleIds = sampleIds;
    }

    public GetDataLinksFromSampleSetParams withSampleIds(List<SampleIdentifier> sampleIds) {
        this.sampleIds = sampleIds;
        return this;
    }

    @JsonProperty("effective_time")
    public Long getEffectiveTime() {
        return effectiveTime;
    }

    @JsonProperty("effective_time")
    public void setEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
    }

    public GetDataLinksFromSampleSetParams withEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
        return this;
    }

    @JsonProperty("as_admin")
    public Long getAsAdmin() {
        return asAdmin;
    }

    @JsonProperty("as_admin")
    public void setAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
    }

    public GetDataLinksFromSampleSetParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("GetDataLinksFromSampleSetParams"+" [sampleIds=")+ sampleIds)+", effectiveTime=")+ effectiveTime)+", asAdmin=")+ asAdmin)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
