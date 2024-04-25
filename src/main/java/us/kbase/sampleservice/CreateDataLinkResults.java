
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CreateDataLinkResults</p>
 * <pre>
 * create_data_link results.
 *         new_link - the new link.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "new_link"
})
public class CreateDataLinkResults {

    /**
     * <p>Original spec-file type: DataLink</p>
     * <pre>
     * A data link from a KBase workspace object to a sample.
     *         upa - the workspace UPA of the linked object.
     *         dataid - the dataid of the linked data, if any, within the object. If omitted the
     *             entire object is linked to the sample.
     *         id - the sample id.
     *         version - the sample version.
     *         node - the sample node.
     *         createdby - the user that created the link.
     *         created - the time the link was created.
     *         expiredby - the user that expired the link, if any.
     *         expired - the time the link was expired, if at all.
     * </pre>
     * 
     */
    @JsonProperty("new_link")
    private DataLink newLink;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: DataLink</p>
     * <pre>
     * A data link from a KBase workspace object to a sample.
     *         upa - the workspace UPA of the linked object.
     *         dataid - the dataid of the linked data, if any, within the object. If omitted the
     *             entire object is linked to the sample.
     *         id - the sample id.
     *         version - the sample version.
     *         node - the sample node.
     *         createdby - the user that created the link.
     *         created - the time the link was created.
     *         expiredby - the user that expired the link, if any.
     *         expired - the time the link was expired, if at all.
     * </pre>
     * 
     */
    @JsonProperty("new_link")
    public DataLink getNewLink() {
        return newLink;
    }

    /**
     * <p>Original spec-file type: DataLink</p>
     * <pre>
     * A data link from a KBase workspace object to a sample.
     *         upa - the workspace UPA of the linked object.
     *         dataid - the dataid of the linked data, if any, within the object. If omitted the
     *             entire object is linked to the sample.
     *         id - the sample id.
     *         version - the sample version.
     *         node - the sample node.
     *         createdby - the user that created the link.
     *         created - the time the link was created.
     *         expiredby - the user that expired the link, if any.
     *         expired - the time the link was expired, if at all.
     * </pre>
     * 
     */
    @JsonProperty("new_link")
    public void setNewLink(DataLink newLink) {
        this.newLink = newLink;
    }

    public CreateDataLinkResults withNewLink(DataLink newLink) {
        this.newLink = newLink;
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
        return ((((("CreateDataLinkResults"+" [newLink=")+ newLink)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
